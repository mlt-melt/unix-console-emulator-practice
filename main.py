import os
import sys
import socket
import argparse
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


def execute_startup_script(script_path: str, vfs_path: str) -> int:
    """
    Execute startup script. Each line is treated as a command.
    Lines starting with # are treated as comments.
    Shows both input and output to simulate user interaction.
    """
    if not os.path.exists(script_path):
        print(f"Error: Startup script not found: {script_path}")
        return 1
    
    print(f"Executing startup script: {script_path}")
    print("-" * 50)
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading startup script: {e}")
        return 1
    
    for line_num, line in enumerate(lines, 1):
        line = line.rstrip('\n\r')
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            if line.startswith('#'):
                print(f"# {line[1:].lstrip()}")  # Show comments
            continue
        
        # Show the command as if user typed it
        prompt = make_prompt()
        print(f"{prompt}{line}")
        
        # Parse and execute the command
        parsed = parse_cmd(line)
        if not parsed:
            continue
            
        cmd, args = parsed
        try:
            cont = handle_command(cmd, args)
            if not cont:
                print("Script terminated with exit command")
                break
        except Exception as e:
            print(f"Error executing line {line_num}: {e}")
            continue
    
    print("-" * 50)
    print("Startup script execution completed")
    return 0


def print_config_debug(vfs_path: str, script_path: str, interactive: bool):
    """
    Print debug information about configuration parameters.
    """
    print("=" * 60)
    print("UNIX CONSOLE EMULATOR - DEBUG CONFIGURATION")
    print("=" * 60)
    print(f"VFS Path: {vfs_path}")
    print(f"Startup Script: {script_path}")
    print(f"Interactive Mode: {interactive}")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {sys.platform}")
    user, host = uname_host()
    print(f"User@Host: {user}@{host}")
    print("=" * 60)
    print()


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="UNIX Console Emulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --vfs /path/to/vfs --script startup.sh
  python main.py --vfs ./virtual_fs --script test.sh --interactive
  python main.py --demo
        """
    )
    
    parser.add_argument(
        '--vfs', 
        type=str, 
        help='Path to the virtual file system root directory'
    )
    
    parser.add_argument(
        '--script', 
        type=str, 
        help='Path to the startup script to execute'
    )
    
    parser.add_argument(
        '--interactive', 
        action='store_true', 
        help='Enter interactive mode after executing startup script'
    )
    
    parser.add_argument(
        '--demo', 
        action='store_true', 
        help='Run scripted demo instead of interactive REPL'
    )
    
    return parser.parse_args()


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


def main():
    """
    Main entry point with argument parsing and configuration.
    """
    args = parse_arguments()
    
    # Debug output of all configuration parameters
    vfs_path = args.vfs or "./virtual_fs"  # Default VFS path
    script_path = args.script
    interactive = args.interactive
    
    if args.demo:
        # Legacy demo mode
        return demo_script()
    
    print_config_debug(vfs_path, script_path, interactive)
    
    exit_code = 0
    
    # Execute startup script if provided
    if script_path:
        exit_code = execute_startup_script(script_path, vfs_path)
        if exit_code != 0 and not interactive:
            return exit_code
    
    # Enter interactive mode if requested or no script provided
    if interactive or not script_path:
        print("Entering interactive mode...")
        print("Type 'exit' to quit.")
        print()
        exit_code = repl()
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
