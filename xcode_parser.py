import os
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple
from config import Config

class TodoItem:
    """Represents a TODO item found in source code."""
    
    def __init__(self, content: str, file_path: str, line_number: int, todo_type: str = "TODO"):
        self.content = content.strip()
        self.file_path = file_path
        self.line_number = line_number
        self.todo_type = todo_type
        self.unique_id = f"{file_path}:{line_number}:{content}"
    
    def __str__(self):
        return f"{self.todo_type}: {self.content} ({self.file_path}:{self.line_number})"
    
    def __eq__(self, other):
        if isinstance(other, TodoItem):
            return self.unique_id == other.unique_id
        return False
    
    def __hash__(self):
        return hash(self.unique_id)

class XcodeParser:
    """Parser for Xcode projects to find TODO statements."""
    
    def __init__(self, config: Config):
        self.config = config
        self.todo_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in config.todo_patterns]
        self.completion_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in config.completion_patterns]
    
    def find_source_files(self, project_path: str) -> List[str]:
        """Find all source files in the Xcode project."""
        source_files = []
        project_path_obj = Path(project_path)
        
        if not project_path_obj.exists():
            print(f"Error: Project path {project_path} does not exist")
            return source_files
        
        # Walk through the project directory
        for root, dirs, files in os.walk(project_path_obj):
            # Skip common directories that shouldn't contain source code
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {
                'build', 'DerivedData', 'Pods', 'node_modules', '.git', '.svn'
            }]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in self.config.source_extensions:
                    source_files.append(str(file_path))
        
        return source_files
    
    def parse_file_for_todos(self, file_path: str) -> List[TodoItem]:
        """Parse a single file for TODO statements."""
        todos = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            for line_number, line in enumerate(lines, 1):
                # Check for TODO patterns
                for pattern in self.todo_patterns:
                    match = pattern.search(line)
                    if match:
                        content = match.group(1).strip()
                        todo_type = "TODO" if "TODO" in line.upper() else "FIXME"
                        todo_item = TodoItem(content, file_path, line_number, todo_type)
                        todos.append(todo_item)
                        break
                        
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
        
        return todos
    
    def parse_file_for_completions(self, file_path: str) -> List[TodoItem]:
        """Parse a single file for completion statements (DONE, COMPLETED)."""
        completions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            for line_number, line in enumerate(lines, 1):
                # Check for completion patterns
                for pattern in self.completion_patterns:
                    match = pattern.search(line)
                    if match:
                        content = match.group(1).strip()
                        completion_type = "DONE" if "DONE" in line.upper() else "COMPLETED"
                        completion_item = TodoItem(content, file_path, line_number, completion_type)
                        completions.append(completion_item)
                        break
                        
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
        
        return completions
    
    def parse_project(self, project_path: str) -> Tuple[List[TodoItem], List[TodoItem]]:
        """Parse an entire Xcode project for TODOs and completions."""
        print(f"Scanning project: {project_path}")
        
        source_files = self.find_source_files(project_path)
        print(f"Found {len(source_files)} source files to scan")
        
        all_todos = []
        all_completions = []
        
        for file_path in source_files:
            todos = self.parse_file_for_todos(file_path)
            completions = self.parse_file_for_completions(file_path)
            
            all_todos.extend(todos)
            all_completions.extend(completions)
            
            if todos or completions:
                print(f"  {file_path}: {len(todos)} TODOs, {len(completions)} completions")
        
        print(f"\nTotal: {len(all_todos)} TODO items, {len(all_completions)} completion items")
        return all_todos, all_completions
    
    def get_todo_content_for_todoist(self, todo_item: TodoItem) -> str:
        """Format TODO content for Todoist task."""
        relative_path = os.path.relpath(todo_item.file_path)
        return f"{todo_item.content} ({relative_path}:{todo_item.line_number})"
    
    def get_todo_description(self, todo_item: TodoItem) -> str:
        """Get description for Todoist task."""
        return f"File: {todo_item.file_path}\nLine: {todo_item.line_number}\nType: {todo_item.todo_type}" 