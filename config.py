import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management for Todoist sync tool."""
    
    def __init__(self):
        self.todoist_api_token = os.getenv('TODOIST_API_TOKEN')
        self.todoist_project_id = os.getenv('TODOIST_PROJECT_ID')
        
        # File extensions to scan for TODOs
        self.source_extensions = {
            '.swift', '.m', '.mm', '.h', '.hpp', '.cpp', '.c',
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.kt'
        }
        
        # TODO patterns to match
        self.todo_patterns = [
            r'//\s*TODO[:\s]+(.+)',
            r'/\*\s*TODO[:\s]+(.+?)\s*\*/',
            r'#\s*TODO[:\s]+(.+)',
            r'//\s*FIXME[:\s]+(.+)',
            r'/\*\s*FIXME[:\s]+(.+?)\s*\*/',
            r'#\s*FIXME[:\s]+(.+)'
        ]
        
        # Completion patterns (when TODO is marked as done)
        self.completion_patterns = [
            r'//\s*DONE[:\s]+(.+)',
            r'/\*\s*DONE[:\s]+(.+?)\s*\*/',
            r'#\s*DONE[:\s]+(.+)',
            r'//\s*COMPLETED[:\s]+(.+)',
            r'/\*\s*COMPLETED[:\s]+(.+?)\s*\*/',
            r'#\s*COMPLETED[:\s]+(.+)'
        ]
    
    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if not self.todoist_api_token:
            print("Error: TODOIST_API_TOKEN not found in environment variables")
            print("Please set it in your .env file or environment")
            return False
        return True
    
    def get_project_id(self) -> Optional[str]:
        """Get the Todoist project ID."""
        return self.todoist_project_id
    
    def set_project_id(self, project_id: str):
        """Set the Todoist project ID."""
        self.todoist_project_id = project_id 