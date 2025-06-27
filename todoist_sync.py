#!/usr/bin/env python3
"""
Todoist Xcode Sync - Main script for syncing TODO statements from Xcode projects to Todoist.
"""

import argparse
import sys
from typing import Set, List
from config import Config
from xcode_parser import XcodeParser, TodoItem
from todoist_client import TodoistClient

class TodoistSync:
    """Main sync orchestrator."""
    
    def __init__(self, config: Config):
        self.config = config
        if not config.todoist_api_token:
            raise ValueError("Todoist API token is required")
        self.todoist_client = TodoistClient(config.todoist_api_token)
        self.parser = XcodeParser(config)
    
    def sync_project(self, project_path: str, dry_run: bool = False) -> bool:
        """Sync TODOs from Xcode project to Todoist."""
        if not self.config.validate():
            return False
        
        project_id = self.config.get_project_id()
        if not project_id:
            print("Error: No Todoist project ID specified")
            print("Use --project-id or set TODOIST_PROJECT_ID in .env file")
            return False
        
        # Parse the Xcode project
        todos, completions = self.parser.parse_project(project_path)
        
        if dry_run:
            return self._dry_run_sync(todos, completions, project_id)
        else:
            return self._perform_sync(todos, completions, project_id)
    
    def _dry_run_sync(self, todos: List[TodoItem], completions: List[TodoItem], project_id: str) -> bool:
        """Preview what changes would be made without actually making them."""
        print("\n=== DRY RUN - Preview of changes ===")
        
        # Get existing tasks from Todoist
        existing_tasks = self.todoist_client.get_tasks(project_id)
        existing_task_contents = {task['content'] for task in existing_tasks}
        
        # Find new TODOs to add
        new_todos = []
        for todo in todos:
            todoist_content = self.parser.get_todo_content_for_todoist(todo)
            if todoist_content not in existing_task_contents:
                new_todos.append(todo)
        
        # Find completed tasks to remove
        completed_tasks = []
        for completion in completions:
            # Look for matching TODO tasks that should be completed
            for task in existing_tasks:
                if completion.content in task['content']:
                    completed_tasks.append(task)
                    break
        
        print(f"\nWould add {len(new_todos)} new TODO tasks:")
        for todo in new_todos:
            print(f"  + {self.parser.get_todo_content_for_todoist(todo)}")
        
        print(f"\nWould complete {len(completed_tasks)} tasks:")
        for task in completed_tasks:
            print(f"  ✓ {task['content']}")
        
        if not new_todos and not completed_tasks:
            print("\nNo changes needed - everything is in sync!")
        
        return True
    
    def _perform_sync(self, todos: List[TodoItem], completions: List[TodoItem], project_id: str) -> bool:
        """Actually perform the sync operations."""
        print("\n=== Performing sync ===")
        
        # Get existing tasks from Todoist
        existing_tasks = self.todoist_client.get_tasks(project_id)
        existing_task_contents = {task['content'] for task in existing_tasks}
        
        # Add new TODOs
        added_count = 0
        for todo in todos:
            todoist_content = self.parser.get_todo_content_for_todoist(todo)
            if todoist_content not in existing_task_contents:
                description = self.parser.get_todo_description(todo)
                task = self.todoist_client.create_task(todoist_content, project_id, description)
                if task:
                    print(f"✓ Added: {todoist_content}")
                    added_count += 1
                else:
                    print(f"✗ Failed to add: {todoist_content}")
        
        # Handle completions
        completed_count = 0
        for completion in completions:
            # Find matching TODO tasks to complete
            for task in existing_tasks:
                if completion.content in task['content'] and not task.get('is_completed', False):
                    if self.todoist_client.close_task(task['id']):
                        print(f"✓ Completed: {task['content']}")
                        completed_count += 1
                    else:
                        print(f"✗ Failed to complete: {task['content']}")
                    break
        
        print(f"\nSync completed:")
        print(f"  Added: {added_count} tasks")
        print(f"  Completed: {completed_count} tasks")
        
        return True
    
    def list_projects(self):
        """List available Todoist projects."""
        self.todoist_client.list_projects()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Sync TODO statements from Xcode projects to Todoist",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python todoist_sync.py /path/to/xcode/project
  python todoist_sync.py /path/to/xcode/project --project-id 123456
  python todoist_sync.py /path/to/xcode/project --dry-run
  python todoist_sync.py --list-projects
        """
    )
    
    parser.add_argument(
        'project_path',
        nargs='?',
        help='Path to the Xcode project directory'
    )
    
    parser.add_argument(
        '--project-id',
        help='Todoist project ID to sync with'
    )
    
    parser.add_argument(
        '--list-projects',
        action='store_true',
        help='List available Todoist projects'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without making them'
    )
    
    args = parser.parse_args()
    
    # Initialize configuration
    config = Config()
    
    # Handle list projects command
    if args.list_projects:
        sync = TodoistSync(config)
        sync.list_projects()
        return
    
    # Validate required arguments
    if not args.project_path:
        parser.error("project_path is required (unless using --list-projects)")
    
    # Set project ID if provided
    if args.project_id:
        config.set_project_id(args.project_id)
    
    # Perform sync
    sync = TodoistSync(config)
    success = sync.sync_project(args.project_path, args.dry_run)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 