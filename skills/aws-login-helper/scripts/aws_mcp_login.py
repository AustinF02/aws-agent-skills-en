"""Authentication checks for AWS MCP. Never prints or stores credentials. Requires Python 3.11+."""
import argparse
import configparser
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import time

WAIT_SECONDS = 180
ENDPOINT = "https://aws-mcp.us-east-1.api.aws/mcp"


def validate(profile, region):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.@+-]{0,127}", profile):
        raise ValueError("Profile names must start with a letter or number and contain at most 128 letters, numbers, or _.@+-.")
    if not re.fullmatch(r"[a-z]{2}(?:-[a-z0-9]+)+-\d+", region):
        raise ValueError("Check the AWS Region name.")


def environment(profile, region):
    env = os.environ.copy()
    # Do not mix the selected profile with temporary credentials from the parent process.
    for key in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN", "AWS_SECURITY_TOKEN"):
        env.pop(key, None)
    env.update(AWS_PROFILE=profile, AWS_MCP_PROXY_PROFILES=profile,
               AWS_REGION=region, AWS_DEFAULT_REGION=region, AWS_PAGER="")
    return env


def check_prerequisites(aws, profile, region):
    result = subprocess.run([aws, "--version"], env=environment(profile, region),
                            capture_output=True, text=True, timeout=20)
    version = re.search(r"aws-cli/(\d+)\.(\d+)\.(\d+)", result.stdout + result.stderr)
    if result.returncode or not version or int(version[1]) != 2 or tuple(
            int(part) for part in version.groups()) < (2, 32, 0):
        raise RuntimeError("AWS CLI v2.32.0 or later in the v2 series is required. Install or update it using the official AWS CLI guide.")

    config = configparser.RawConfigParser()
    credentials = configparser.RawConfigParser()
    try:
        for parser, variable, filename in (
                (config, "AWS_CONFIG_FILE", "config"),
                (credentials, "AWS_SHARED_CREDENTIALS_FILE", "credentials")):
            path = Path(os.environ.get(variable, str(Path.home()/".aws"/filename))).expanduser()
            try:
                with path.open(encoding="utf-8") as stream:
                    parser.read_file(stream)
            except FileNotFoundError:
                pass
    except (OSError, UnicodeError, configparser.Error):
        raise RuntimeError("AWS profile configuration cannot be read safely. Check its format and file access; no sign-in was started.") from None

    section = "default" if profile == "default" else "profile " + profile
    if not config.has_section(section):
        raise RuntimeError("The selected profile is not configured for this helper. Complete an authorized first-time named-profile sign-in before enabling automation.")
    settings = config[section]
    incompatible = {"role_arn", "source_profile", "credential_source", "credential_process",
                    "web_identity_token_file", "aws_access_key_id", "aws_secret_access_key",
                    "aws_session_token", "aws_security_token"}
    if (incompatible.intersection(settings) or any(key.startswith("sso_") for key in settings)
            or credentials.has_section(profile)):
        raise RuntimeError("The selected profile has another or mixed authentication configuration. Keep its existing SSO, key, process, or role workflow; do not use this helper.")
    if not settings.get("login_session", "").strip():
        raise RuntimeError("The selected profile has no login_session. Complete an authorized first-time aws login for this named profile before enabling automation.")


def check_auth(aws, profile, region):
    result = subprocess.run(
        [aws, "sts", "get-caller-identity", "--profile", profile, "--region", region,
         "--query", "Account != "+chr(96)+"null"+chr(96), "--output", "text", "--no-cli-pager"],
        env=environment(profile, region), capture_output=True, text=True, timeout=20)
    if result.returncode == 0:
        return True
    expired = ("refresh token has expired", "session has expired", "loginrefreshrequired",
               "expiredtoken", "unable to locate credentials")
    if any(message in result.stderr.lower() for message in expired):
        return False
    raise RuntimeError("AWS access check failed. Check your network, permissions, and profile settings. Automatic sign-in will not run.")


def login(aws, profile, region):
    if sys.stdin.isatty():
        result = subprocess.run([aws, "login", "--profile", profile, "--region", region],
                                env=environment(profile, region), timeout=WAIT_SECONDS)
        if result.returncode:
            raise RuntimeError("Sign-in failed or was canceled.")
        return
    if sys.platform != "darwin":
        raise RuntimeError("Automatic sign-in from a GUI app is not supported on this OS. Run this helper in a terminal with --login-only, then reconnect the MCP server.")
    command = shlex.join([sys.executable, str(Path(__file__).resolve()),
                         "--profile", profile, "--region", region, "--login-only"])
    apple = 'tell application "Terminal"\nactivate\ndo script '+json.dumps(command)+'\nend tell'
    subprocess.run(["/usr/bin/osascript", "-e", apple], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
    print("AWS sign-in opened in Terminal. Complete browser authentication within 3 minutes.", file=sys.stderr)
    deadline = time.monotonic()+WAIT_SECONDS
    while time.monotonic() < deadline:
        time.sleep(3)
        if check_auth(aws, profile, region):
            return
    raise RuntimeError("The sign-in wait timed out. Finish authentication, then reconnect the MCP server.")


@contextmanager
def login_lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        os.chmod(path, 0o600)
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        deadline = time.monotonic()+WAIT_SECONDS
        while True:
            try:
                if os.name == "nt":
                    import msvcrt
                    stream.seek(0)
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except (BlockingIOError, OSError):
                if time.monotonic() >= deadline:
                    raise RuntimeError("Another AWS sign-in is still pending. Reconnect the MCP server after authentication finishes.")
                time.sleep(1)
        try:
            yield
        finally:
            if os.name == "nt":
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def ensure_auth(aws, profile, region, cache=None):
    cache = cache or Path.home()/".cache"/"aws-agent-skills-ja"
    name = hashlib.sha256(profile.encode()).hexdigest()[:24]+".lock"
    with login_lock(cache/name):
        if not check_auth(aws, profile, region):
            login(aws, profile, region)
            if not check_auth(aws, profile, region):
                raise RuntimeError("AWS access is still unavailable after sign-in.")


def main():
    parser = argparse.ArgumentParser(description="Check AWS authentication and start AWS MCP")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--region", required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Check authentication only; do not sign in or start MCP")
    mode.add_argument("--login-only", action="store_true", help="Run interactive sign-in in a terminal without starting MCP")
    args = parser.parse_args()
    validate(args.profile, args.region)
    aws = shutil.which("aws")
    if not aws:
        raise RuntimeError("AWS CLI was not found on PATH. Set up AWS CLI v2.32 or later.")
    check_prerequisites(aws, args.profile, args.region)
    if args.check:
        if not check_auth(aws, args.profile, args.region):
            raise RuntimeError("Your AWS session has expired. Authenticate again with --login-only.")
        print("AWS authentication check: passed")
        return
    if args.login_only:
        login(aws, args.profile, args.region)
        if not check_auth(aws, args.profile, args.region):
            raise RuntimeError("The access check failed after sign-in.")
        return
    uvx = shutil.which("uvx")
    if not uvx:
        raise RuntimeError("uvx was not found on PATH. Set up uv.")
    ensure_auth(aws, args.profile, args.region)
    os.execvpe(uvx, [uvx, "mcp-proxy-for-aws-cli@latest", ENDPOINT],
               environment(args.profile, args.region))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
    except Exception:
        # Full SDK and OS exceptions may contain identifying information.
        print("The AWS login helper failed. Check the required tools and your connection.", file=sys.stderr)
        sys.exit(1)
