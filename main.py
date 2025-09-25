import os
import sys
import socket
import argparse
import json
import base64
from typing import List, Tuple, Optional, Dict, Any


class VFS:
    """
    Virtual File System implementation.
    Stores all data in memory, loads from JSON format.
    """
    
    def __init__(self, vfs_path: str = None):
        self.current_dir = "/"
        self.data: Dict[str, Any] = {
            "/": {
                "type": "directory",
                "children": {}
            }
        }
        if vfs_path and os.path.exists(vfs_path):
            self.load_from_file(vfs_path)
        self.vfs_file_path = vfs_path
    
    def load_from_file(self, file_path: str):
        """Load VFS from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            # Ensure root directory exists
            if "/" not in self.data:
                self.data["/"] = {"type": "directory", "children": {}}
        except Exception as e:
            print(f"Warning: Could not load VFS from {file_path}: {e}")
            print("Using empty VFS")
    
    def save_to_file(self, file_path: str):
        """Save VFS to JSON file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving VFS to {file_path}: {e}")
            return False
    
    def normalize_path(self, path: str) -> str:
        """Normalize path to absolute form."""
        if not path.startswith('/'):
            # Relative path
            if self.current_dir == '/':
                path = '/' + path
            else:
                path = self.current_dir + '/' + path
        
        # Normalize path (remove . and ..)
        parts = []
        for part in path.split('/'):
            if part == '' or part == '.':
                continue
            elif part == '..':
                if parts:
                    parts.pop()
            else:
                parts.append(part)
        
        result = '/' + '/'.join(parts) if parts else '/'
        return result
    
    def exists(self, path: str) -> bool:
        """Check if path exists in VFS."""
        normalized = self.normalize_path(path)
        return normalized in self.data
    
    def is_directory(self, path: str) -> bool:
        """Check if path is a directory."""
        normalized = self.normalize_path(path)
        if normalized not in self.data:
            return False
        return self.data[normalized].get("type") == "directory"
    
    def is_file(self, path: str) -> bool:
        """Check if path is a file."""
        normalized = self.normalize_path(path)
        if normalized not in self.data:
            return False
        return self.data[normalized].get("type") == "file"
    
    def list_directory(self, path: str = None) -> List[str]:
        """List contents of directory."""
        if path is None:
            path = self.current_dir
        
        normalized = self.normalize_path(path)
        if not self.exists(normalized):
            return []
        
        if not self.is_directory(normalized):
            return []
        
        children = self.data[normalized].get("children", {})
        return list(children.keys())
    
    def change_directory(self, path: str) -> bool:
        """Change current directory."""
        normalized = self.normalize_path(path)
        if not self.exists(normalized):
            print(f"cd: {path}: No such file or directory")
            return False
        
        if not self.is_directory(normalized):
            print(f"cd: {path}: Not a directory")
            return False
        
        self.current_dir = normalized
        return True
    
    def get_file_content(self, path: str) -> Optional[str]:
        """Get file content (decode base64 if needed)."""
        normalized = self.normalize_path(path)
        if not self.exists(normalized) or not self.is_file(normalized):
            return None
        
        file_data = self.data[normalized]
        content = file_data.get("content", "")
        
        # If content is base64 encoded
        if file_data.get("encoding") == "base64":
            try:
                return base64.b64decode(content).decode('utf-8')
            except:
                return content  # Return as is if decode fails
        
        return content
    
    def create_file(self, path: str, content: str = "", encoding: str = "text"):
        """Create a new file in VFS."""
        normalized = self.normalize_path(path)
        parent_path = '/'.join(normalized.split('/')[:-1]) or '/'
        
        if not self.exists(parent_path) or not self.is_directory(parent_path):
            print(f"Cannot create file {path}: parent directory does not exist")
            return False
        
        # Encode content if binary
        if encoding == "base64":
            try:
                encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            except:
                encoded_content = content
        else:
            encoded_content = content
        
        self.data[normalized] = {
            "type": "file",
            "content": encoded_content,
            "encoding": encoding
        }
        
        # Add to parent directory
        filename = normalized.split('/')[-1]
        self.data[parent_path]["children"][filename] = normalized
        return True
    
    def create_directory(self, path: str):
        """Create a new directory in VFS."""
        normalized = self.normalize_path(path)
        parent_path = '/'.join(normalized.split('/')[:-1]) or '/'
        
        if not self.exists(parent_path) or not self.is_directory(parent_path):
            print(f"Cannot create directory {path}: parent directory does not exist")
            return False
        
        if self.exists(normalized):
            print(f"Directory {path} already exists")
            return False
        
        self.data[normalized] = {
            "type": "directory",
            "children": {}
        }
        
        # Add to parent directory
        dirname = normalized.split('/')[-1]
        self.data[parent_path]["children"][dirname] = normalized
        return True


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


def make_prompt(vfs: VFS = None) -> str:
    user, host = uname_host()
    if vfs:
        path_part = vfs.current_dir
    else:
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


def handle_command(cmd: str, args: List[str], vfs: VFS = None) -> bool:
    """
    Handle a single command.
    Returns True to continue the loop, False to exit.
    """
    if cmd == "exit":
        return False
    
    if cmd == "ls":
        if vfs:
            path = args[0] if args else None
            items = vfs.list_directory(path)
            if items:
                for item in sorted(items):
                    item_path = vfs.normalize_path((path or vfs.current_dir) + '/' + item)
                    if vfs.is_directory(item_path):
                        print(f"{item}/")
                    else:
                        print(item)
            # Empty directory is valid, no output
        else:
            # Fallback for when VFS is not available
            if args:
                print(f"ls called with args: {' '.join(args)}")
            else:
                print("ls called with no args")
        return True
    
    if cmd == "cd":
        if vfs:
            if args:
                vfs.change_directory(args[0])
            else:
                vfs.change_directory("/")  # cd without args goes to root
        else:
            # Fallback for when VFS is not available
            if args:
                print(f"cd called with args: {' '.join(args)}")
            else:
                print("cd called with no args")
        return True
    
    if cmd == "cat":
        if vfs and args:
            content = vfs.get_file_content(args[0])
            if content is not None:
                print(content)
            else:
                print(f"cat: {args[0]}: No such file or directory")
        else:
            print("cat: missing file operand")
        return True
    
    if cmd == "pwd":
        if vfs:
            print(vfs.current_dir)
        else:
            print("/")  # Fallback
        return True
    
    if cmd == "mkdir":
        if vfs and args:
            for dir_name in args:
                vfs.create_directory(dir_name)
        else:
            print("mkdir: missing operand")
        return True
    
    if cmd == "touch":
        if vfs and args:
            for file_name in args:
                vfs.create_file(file_name)
        else:
            print("touch: missing file operand")
        return True
    
    if cmd == "vfs-save":
        if vfs and args:
            if vfs.save_to_file(args[0]):
                print(f"VFS saved to {args[0]}")
            else:
                print(f"Failed to save VFS to {args[0]}")
        else:
            print("vfs-save: missing file path")
        return True
    
    # Unknown command -> error
    print(f"Command not found: {cmd}")
    return True


def repl(vfs: VFS = None) -> int:
    # REPL loop with basic error handling
    while True:
        try:
            prompt = make_prompt(vfs)
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
            cont = handle_command(cmd, args, vfs)
            if not cont:
                return 0
        except Exception as e:
            print(f"Error: {e}")
            continue


def execute_startup_script(script_path: str, vfs_path: str, vfs: VFS = None) -> int:
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
        prompt = make_prompt(vfs)
        print(f"{prompt}{line}")
        
        # Parse and execute the command
        parsed = parse_cmd(line)
        if not parsed:
            continue
            
        cmd, args = parsed
        try:
            cont = handle_command(cmd, args, vfs)
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


def demo_script(vfs: VFS = None) -> int:
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
        prompt = make_prompt(vfs)
        print(prompt + line)
        parsed = parse_cmd(line)
        if not parsed:
            continue
        cmd, args = parsed
        cont = handle_command(cmd, args, vfs)
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
    
    # Initialize VFS
    vfs = VFS(vfs_path)
    
    if args.demo:
        # Legacy demo mode
        return demo_script(vfs)
    
    print_config_debug(vfs_path, script_path, interactive)
    
    exit_code = 0
    
    # Execute startup script if provided
    if script_path:
        exit_code = execute_startup_script(script_path, vfs_path, vfs)
        if exit_code != 0 and not interactive:
            return exit_code
    
    # Enter interactive mode if requested or no script provided
    if interactive or not script_path:
        print("Entering interactive mode...")
        print("Type 'exit' to quit.")
        print()
        exit_code = repl(vfs)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
