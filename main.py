import os
import sys
import socket
from typing import List, Tuple, Optional


def uname_host() -> Tuple[str, str]:
    # Try to get username in a cross-platform way
    user = (
        os.environ.get("USER")
        or os.environ.get("USERNAME")
        or os.environ.get("LOGNAME")
        or "user"
    )
    try:
        host = socket.gethostname() or "host"
    except Exception:
        host = "host"
    return user, host


def tilde_path(cwd: str) -> str:
    # Represent home as ~ and normalize separators to UNIX style
    try:
        home = os.path.expanduser("~")
    except Exception:
        home = None
    if home and cwd.startswith(home):
        shown = "~" + cwd[len(home):]
    else:
        shown = cwd
    # Use forward slashes for UNIX-like look
    return shown.replace("\\", "/")


def make_prompt() -> str:
    user, host = uname_host()
    try:
        cwd = os.getcwd()
    except Exception:
        cwd = "/"
    path_part = tilde_path(cwd)
    return f"{user}@{host}:{path_part}$ "


def parse_cmd(line: str) -> Optional[Tuple[str, List[str]]]:
    # Simple parser: split by whitespace; ignore empty input
    tokens = line.strip().split()
    if not tokens:
        return None
    return tokens[0], tokens[1:]


def handle_command(cmd: str, args: List[str]) -> bool:
    """
    Handle a single command.
    Returns True to continue the loop, False to exit.
    """
    if cmd == "exit":
        return False
    if cmd in ("ls", "cd"):
        # Stubs per Stage 1: just echo command and args
        if args:
            print(f"{cmd} called with args: {' '.join(args)}")
        else:
            print(f"{cmd} called with no args")
        return True
    # Unknown command -> error
    print(f"Command not found: {cmd}")
    return True


def repl() -> int:
    # REPL loop with basic error handling
    while True:
        try:
            prompt = make_prompt()
            line = input(prompt)
        except KeyboardInterrupt:
            # ^C -> new line, continue
            print()
            continue
        except EOFError:
            # Ctrl+Z/Ctrl+D -> exit
            print()
            return 0

        parsed = parse_cmd(line)
        if not parsed:
            # empty line -> continue
            continue
        cmd, args = parsed
        try:
            cont = handle_command(cmd, args)
            if not cont:
                return 0
        except Exception as e:
            print(f"Error: {e}")
            continue


def demo_script() -> int:
    """
    Non-interactive demonstration for CI/docs:
    Runs through a short script to showcase features and error handling.
    """
    script = [
        "",  # empty input
        "ls",
        "ls src docs",
        "cd /tmp",
        "unknown",
        "exit",
    ]
    for line in script:
        prompt = make_prompt()
        print(prompt + line)
        parsed = parse_cmd(line)
        if not parsed:
            continue
        cmd, args = parsed
        cont = handle_command(cmd, args)
        if not cont:
            return 0
    return 0


if __name__ == "__main__":
    # Optional flags:
    #   --demo : run scripted demo instead of interactive REPL
    if "--demo" in sys.argv:
        sys.exit(demo_script())
    sys.exit(repl())
