import requests
import json
from typing import List, Dict, Optional
from datetime import datetime

class TodoistClient:
    """Client for interacting with Todoist API."""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.todoist.com/rest/v2"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def get_projects(self) -> List[Dict]:
        """Get all projects from Todoist."""
        try:
            response = requests.get(f"{self.base_url}/projects", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching projects: {e}")
            return []
    
    def get_tasks(self, project_id: str) -> List[Dict]:
        """Get all tasks from a specific project."""
        try:
            params = {"project_id": project_id}
            response = requests.get(f"{self.base_url}/tasks", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching tasks: {e}")
            return []
    
    def create_task(self, content: str, project_id: str, description: str = "") -> Optional[Dict]:
        """Create a new task in Todoist."""
        try:
            data = {
                "content": content,
                "project_id": project_id,
                "description": description
            }
            response = requests.post(f"{self.base_url}/tasks", headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating task: {e}")
            return None
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task from Todoist."""
        try:
            response = requests.delete(f"{self.base_url}/tasks/{task_id}", headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting task: {e}")
            return False
    
    def close_task(self, task_id: str) -> bool:
        """Close (complete) a task in Todoist."""
        try:
            response = requests.post(f"{self.base_url}/tasks/{task_id}/close", headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error closing task: {e}")
            return False
    
    def update_task(self, task_id: str, content: Optional[str] = None, description: Optional[str] = None) -> Optional[Dict]:
        """Update an existing task."""
        try:
            data = {}
            if content:
                data["content"] = content
            if description:
                data["description"] = description
            
            response = requests.post(f"{self.base_url}/tasks/{task_id}", headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating task: {e}")
            return None
    
    def find_task_by_content(self, content: str, project_id: str) -> Optional[Dict]:
        """Find a task by its content in a specific project."""
        tasks = self.get_tasks(project_id)
        for task in tasks:
            if task.get("content") == content:
                return task
        return None
    
    def list_projects(self):
        """List all available projects."""
        projects = self.get_projects()
        if not projects:
            print("No projects found or error occurred.")
            return
        
        print("\nAvailable Todoist projects:")
        print("-" * 50)
        for project in projects:
            print(f"ID: {project['id']} | Name: {project['name']}")
            if project.get('parent_id'):
                print(f"  Parent: {project['parent_id']}")
        print("-" * 50) 