#!/usr/bin/env python3
"""
Command registry and implementations for PyTerminal
Handles all terminal commands and their execution
"""

import os
import shutil
import subprocess
import psutil
from pathlib import Path
from typing import List, Tuple, Callable, Dict, Any
import stat

class CommandRegistry:
    """Registry for managing and executing terminal commands"""
    
    def __init__(self):
        self.commands: Dict[str, Callable] = {
            # File system commands
            'ls': self._cmd_ls,
            'cd': self._cmd_cd,
            'pwd': self._cmd_pwd,
            'mkdir': self._cmd_mkdir,
            'rm': self._cmd_rm,
            'cat': self._cmd_cat,
            'touch': self._cmd_touch,
            'cp': self._cmd_cp,
            'mv': self._cmd_mv,
            'rmdir': self._cmd_rmdir,
            'echo': self._cmd_echo,
            
            # System monitoring commands
            'cpu': self._cmd_cpu,
            'mem': self._cmd_mem,
            'ps': self._cmd_ps,
            'disk': self._cmd_disk,
        }
    
    def execute(self, command: str, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Execute a command with given arguments"""
        if command not in self.commands:
            return False, f"Command '{command}' not found. Type 'help' for available commands."
        
        try:
            return self.commands[command](args, current_dir)
        except Exception as e:
            return False, f"Error executing '{command}': {str(e)}"
    
    def _cmd_ls(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """List files and directories"""
        path = args[0] if args else current_dir
        
        # Handle relative paths
        if not os.path.isabs(path):
            path = os.path.join(current_dir, path)
        
        try:
            if not os.path.exists(path):
                return False, f"ls: cannot access '{path}': No such file or directory"
            
            if not os.path.isdir(path):
                return False, f"ls: cannot access '{path}': Not a directory"
            
            items = os.listdir(path)
            if not items:
                return True, ""
            
            # Format output similar to ls -la
            output_lines = []
            for item in sorted(items):
                item_path = os.path.join(path, item)
                try:
                    stat_info = os.stat(item_path)
                    mode = stat.filemode(stat_info.st_mode)
                    size = stat_info.st_size
                    modified = stat_info.st_mtime
                    
                    # Format permissions, size, and name
                    output_lines.append(f"{mode} {size:8d} {item}")
                except OSError:
                    output_lines.append(f"????????? {item}")
            
            return True, "\n".join(output_lines)
        
        except PermissionError:
            return False, f"ls: cannot open directory '{path}': Permission denied"
        except Exception as e:
            return False, f"ls: {str(e)}"
    
    def _cmd_cd(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Change directory"""
        if not args:
            # Go to home directory
            new_dir = os.path.expanduser("~")
        else:
            path = args[0]
            if not os.path.isabs(path):
                new_dir = os.path.join(current_dir, path)
            else:
                new_dir = path
        
        try:
            if not os.path.exists(new_dir):
                return False, f"cd: {new_dir}: No such file or directory"
            
            if not os.path.isdir(new_dir):
                return False, f"cd: {new_dir}: Not a directory"
            
            # Update current directory in the calling context
            os.chdir(new_dir)
            return True, ""
        
        except PermissionError:
            return False, f"cd: {new_dir}: Permission denied"
        except Exception as e:
            return False, f"cd: {str(e)}"
    
    def _cmd_pwd(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Print current working directory"""
        return True, os.getcwd()
    
    def _cmd_mkdir(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Create directory"""
        if not args:
            return False, "mkdir: missing operand"
        
        for dir_name in args:
            if not os.path.isabs(dir_name):
                dir_path = os.path.join(current_dir, dir_name)
            else:
                dir_path = dir_name
            
            try:
                os.makedirs(dir_path, exist_ok=True)
            except FileExistsError:
                return False, f"mkdir: cannot create directory '{dir_name}': File exists"
            except PermissionError:
                return False, f"mkdir: cannot create directory '{dir_name}': Permission denied"
            except Exception as e:
                return False, f"mkdir: {str(e)}"
        
        return True, ""
    
    def _cmd_rm(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Remove file or directory"""
        if not args:
            return False, "rm: missing operand"
        
        for item in args:
            if not os.path.isabs(item):
                item_path = os.path.join(current_dir, item)
            else:
                item_path = item
            
            try:
                if not os.path.exists(item_path):
                    return False, f"rm: cannot remove '{item}': No such file or directory"
                
                if os.path.isdir(item_path):
                    # Safety check for directories
                    try:
                        # Check if directory is empty
                        if os.listdir(item_path):
                            return False, f"rm: cannot remove '{item}': Directory not empty (use 'rm -r' for recursive removal)"
                    except OSError:
                        pass
                    
                    # For empty directories, use rmdir
                    os.rmdir(item_path)
                else:
                    os.remove(item_path)
            
            except PermissionError:
                return False, f"rm: cannot remove '{item}': Permission denied"
            except OSError as e:
                return False, f"rm: {str(e)}"
        
        return True, ""
    
    def _cmd_cat(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Display file contents"""
        if not args:
            return False, "cat: missing operand"
        
        file_path = args[0]
        if not os.path.isabs(file_path):
            file_path = os.path.join(current_dir, file_path)
        
        try:
            if not os.path.exists(file_path):
                return False, f"cat: {file_path}: No such file or directory"
            
            if not os.path.isfile(file_path):
                return False, f"cat: {file_path}: Is a directory"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return True, content
        
        except PermissionError:
            return False, f"cat: {file_path}: Permission denied"
        except Exception as e:
            return False, f"cat: {str(e)}"
    
    def _cmd_touch(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Create empty file"""
        if not args:
            return False, "touch: missing operand"
        
        for file_name in args:
            if not os.path.isabs(file_name):
                file_path = os.path.join(current_dir, file_name)
            else:
                file_path = file_name
            
            try:
                Path(file_path).touch()
            except Exception as e:
                return False, f"touch: {str(e)}"
        
        return True, ""
    
    def _cmd_cp(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Copy file or directory"""
        if len(args) < 2:
            return False, "cp: missing file operand"
        
        src = args[0]
        dest = args[1]
        
        if not os.path.isabs(src):
            src = os.path.join(current_dir, src)
        if not os.path.isabs(dest):
            dest = os.path.join(current_dir, dest)
        
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)
            
            return True, ""
        
        except Exception as e:
            return False, f"cp: {str(e)}"
    
    def _cmd_mv(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Move/rename file or directory"""
        if len(args) < 2:
            return False, "mv: missing file operand"
        
        src = args[0]
        dest = args[1]
        
        if not os.path.isabs(src):
            src = os.path.join(current_dir, src)
        if not os.path.isabs(dest):
            dest = os.path.join(current_dir, dest)
        
        try:
            shutil.move(src, dest)
            return True, ""
        
        except Exception as e:
            return False, f"mv: {str(e)}"
    
    def _cmd_rmdir(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Remove empty directory"""
        if not args:
            return False, "rmdir: missing operand"
        
        for dir_name in args:
            if not os.path.isabs(dir_name):
                dir_path = os.path.join(current_dir, dir_name)
            else:
                dir_path = dir_name
            
            try:
                if not os.path.exists(dir_path):
                    return False, f"rmdir: failed to remove '{dir_name}': No such file or directory"
                
                if not os.path.isdir(dir_path):
                    return False, f"rmdir: failed to remove '{dir_name}': Not a directory"
                
                os.rmdir(dir_path)
            
            except OSError as e:
                return False, f"rmdir: {str(e)}"
        
        return True, ""
    
    def _cmd_echo(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Echo text to output"""
        if not args:
            return True, ""
        
        # Join all arguments with spaces
        text = " ".join(args)
        
        # Handle redirection (simple > filename)
        if ">" in text:
            parts = text.split(">", 1)
            if len(parts) == 2:
                content = parts[0].strip()
                filename = parts[1].strip()
                
                if not os.path.isabs(filename):
                    filename = os.path.join(current_dir, filename)
                
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return True, ""
                except Exception as e:
                    return False, f"echo: {str(e)}"
        
        return True, text
    
    def _cmd_cpu(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Show CPU usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            output = f"CPU Usage: {cpu_percent}%\n"
            output += f"CPU Cores: {cpu_count}\n"
            if cpu_freq:
                output += f"CPU Frequency: {cpu_freq.current:.2f} MHz\n"
            
            return True, output
        
        except Exception as e:
            return False, f"cpu: {str(e)}"
    
    def _cmd_mem(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Show memory usage"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            output = f"Memory Usage: {memory.percent}%\n"
            output += f"Total Memory: {memory.total / (1024**3):.2f} GB\n"
            output += f"Available Memory: {memory.available / (1024**3):.2f} GB\n"
            output += f"Used Memory: {memory.used / (1024**3):.2f} GB\n"
            output += f"Swap Usage: {swap.percent}%\n"
            
            return True, output
        
        except Exception as e:
            return False, f"mem: {str(e)}"
    
    def _cmd_ps(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """List running processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by PID
            processes.sort(key=lambda x: x['pid'])
            
            output = f"{'PID':<8} {'Name':<20} {'CPU%':<8} {'Memory%':<10}\n"
            output += "-" * 50 + "\n"
            
            for proc in processes[:20]:  # Show first 20 processes
                output += f"{proc['pid']:<8} {proc['name']:<20} {proc['cpu_percent']:<8.1f} {proc['memory_percent']:<10.1f}\n"
            
            if len(processes) > 20:
                output += f"... and {len(processes) - 20} more processes\n"
            
            return True, output
        
        except Exception as e:
            return False, f"ps: {str(e)}"
    
    def _cmd_disk(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
        """Show disk usage"""
        try:
            disk_usage = psutil.disk_usage('/')
            partitions = psutil.disk_partitions()
            
            output = f"Disk Usage (Root):\n"
            output += f"Total: {disk_usage.total / (1024**3):.2f} GB\n"
            output += f"Used: {disk_usage.used / (1024**3):.2f} GB\n"
            output += f"Free: {disk_usage.free / (1024**3):.2f} GB\n"
            output += f"Usage: {(disk_usage.used / disk_usage.total) * 100:.1f}%\n\n"
            
            output += "Partitions:\n"
            output += f"{'Device':<15} {'Mountpoint':<20} {'Fstype':<10} {'Total':<12} {'Used':<12} {'Free':<12}\n"
            output += "-" * 80 + "\n"
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    total_gb = usage.total / (1024**3)
                    used_gb = usage.used / (1024**3)
                    free_gb = usage.free / (1024**3)
                    
                    output += f"{partition.device:<15} {partition.mountpoint:<20} {partition.fstype:<10} "
                    output += f"{total_gb:<12.1f} {used_gb:<12.1f} {free_gb:<12.1f}\n"
                except PermissionError:
                    continue
            
            return True, output
        
        except Exception as e:
            return False, f"disk: {str(e)}"
