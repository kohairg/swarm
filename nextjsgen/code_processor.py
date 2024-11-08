from typing import Dict, List
import os
import json
from datetime import datetime
from database import get_db_session, Project

class CodeProcessor:
    def __init__(self):
        self.db = get_db_session()
        self.projects_dir = os.path.join(os.path.dirname(__file__), 'generated')
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)

    def read_project_files(self, project_name: str) -> Dict:
        """Read all files in a project for context."""
        try:
            project = self.db.query(Project).filter(Project.name == project_name).first()
            if not project:
                return {"error": "Project not found"}

            project_files = {}
            for root, _, files in os.walk(project.project_path):
                for file in files:
                    if file.endswith(('.ts', '.tsx', '.js', '.jsx', '.css', '.json')):
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, project.project_path)
                        with open(file_path, 'r') as f:
                            project_files[relative_path] = f.read()

            return project_files
        except Exception as e:
            print(f"Error reading project files: {str(e)}")
            return {"error": str(e)}

    def edit_file(self, project_name: str, file_path: str, content: str) -> Dict:
        """Edit a specific file in the project."""
        try:
            project = self.db.query(Project).filter(Project.name == project_name).first()
            if not project:
                return {"error": "Project not found"}

            full_path = os.path.join(project.project_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w') as f:
                f.write(content)

            project.updated_at = datetime.utcnow()
            self.db.commit()

            return {"status": "success", "message": f"Updated {file_path}"}
        except Exception as e:
            print(f"Error editing file: {str(e)}")
            return {"error": str(e)}

    def create_component(self, project_name: str, component_name: str, content: str) -> Dict:
        """Create a new React component."""
        try:
            project = self.db.query(Project).filter(Project.name == project_name).first()
            if not project:
                return {"error": "Project not found"}

            component_path = f"src/components/{component_name}.tsx"
            full_path = os.path.join(project.project_path, component_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, 'w') as f:
                f.write(content)

            # Update project metadata
            components = project.components or {}
            components[component_name] = {
                "path": component_path,
                "created_at": datetime.utcnow().isoformat()
            }
            project.components = components
            project.updated_at = datetime.utcnow()
            self.db.commit()

            return {"status": "success", "message": f"Created component {component_name}"}
        except Exception as e:
            print(f"Error creating component: {str(e)}")
            return {"error": str(e)}

    def create_page(self, project_name: str, page_name: str, content: str) -> Dict:
        """Create a new Next.js page."""
        try:
            project = self.db.query(Project).filter(Project.name == project_name).first()
            if not project:
                return {"error": "Project not found"}

            page_path = f"src/app/{page_name}/page.tsx"
            full_path = os.path.join(project.project_path, page_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, 'w') as f:
                f.write(content)

            # Update project metadata
            pages = project.pages or {}
            pages[page_name] = {
                "path": page_path,
                "created_at": datetime.utcnow().isoformat()
            }
            project.pages = pages
            project.updated_at = datetime.utcnow()
            self.db.commit()

            return {"status": "success", "message": f"Created page {page_name}"}
        except Exception as e:
            print(f"Error creating page: {str(e)}")
            return {"error": str(e)}

    def __del__(self):
        """Cleanup when the processor is destroyed."""
        if hasattr(self, 'db'):
            self.db.close() 