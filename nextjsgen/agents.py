from typing import Optional, Dict, List
from datetime import datetime
from database import get_db_session, Project
from sqlalchemy import or_, func
import subprocess
import os
import json

class ProjectAgent:
    def __init__(self):
        self.db = get_db_session()
        self.projects_dir = os.path.join(os.path.dirname(__file__), 'generated')
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)

    def create_project(self, name: str, description: str) -> Dict:
        """Create a new NextJS project."""
        try:
            # Create project directory
            project_dir = os.path.join(self.projects_dir, name)
            if not os.path.exists(project_dir):
                os.makedirs(project_dir)
                
            # Initialize NextJS project
            subprocess.run(['npx', 'create-next-app@latest', name, 
                          '--typescript', '--tailwind', '--eslint',
                          '--app', '--src-dir', '--use-npm'],
                          cwd=self.projects_dir, check=True)

            # Store project in database
            project = Project(
                name=name,
                description=description,
                created_at=datetime.utcnow(),
                project_path=project_dir,
                config={}
            )
            self.db.add(project)
            self.db.commit()

            return {
                'status': 'success',
                'message': f'Created project {name}',
                'project_dir': project_dir
            }
        except Exception as e:
            print(f"Error creating project: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def update_project(self, name: str, changes: Dict) -> Dict:
        """Update an existing NextJS project with new changes."""
        try:
            project = self.db.query(Project).filter(Project.name == name).first()
            if not project:
                return {'status': 'error', 'message': 'Project not found'}

            # Apply changes to project files
            for file_path, content in changes.get('files', {}).items():
                full_path = os.path.join(project.project_path, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(content)

            # Update dependencies if needed
            if 'dependencies' in changes:
                subprocess.run(['npm', 'install', *changes['dependencies']], 
                             cwd=project.project_path, check=True)

            return {'status': 'success', 'message': f'Updated project {name}'}
        except Exception as e:
            print(f"Error updating project: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def deploy_project(self, name: str) -> Dict:
        """Deploy a NextJS project to development environment."""
        try:
            project = self.db.query(Project).filter(Project.name == name).first()
            if not project:
                return {'status': 'error', 'message': 'Project not found'}

            # Build and start the project in development mode
            subprocess.run(['docker', 'compose', 'up', '-d', '--build'], 
                         cwd=project.project_path, check=True)

            return {
                'status': 'success',
                'message': f'Deployed project {name}',
                'url': 'http://localhost:3000'
            }
        except Exception as e:
            print(f"Error deploying project: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def list_projects(self) -> List[Dict]:
        """List all NextJS projects."""
        try:
            projects = self.db.query(Project).all()
            return [{
                'name': p.name,
                'description': p.description,
                'created_at': p.created_at.isoformat(),
                'project_path': p.project_path
            } for p in projects]
        except Exception as e:
            print(f"Error listing projects: {str(e)}")
            return []

    def __del__(self):
        """Cleanup when the agent is destroyed."""
        if hasattr(self, 'db'):
            self.db.close() 