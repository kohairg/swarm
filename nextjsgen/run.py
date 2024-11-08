from swarm import Agent
import os
from agents import ProjectAgent
from code_processor import CodeProcessor

def create_project(name: str, description: str):
    """Create a new NextJS project."""
    agent = ProjectAgent()
    return agent.create_project(name, description)

def update_project(name: str, changes: dict):
    """Update an existing NextJS project."""
    agent = ProjectAgent()
    return agent.update_project(name, changes)

def deploy_project(name: str):
    """Deploy a NextJS project."""
    agent = ProjectAgent()
    return agent.deploy_project(name)

def list_projects():
    """List all projects."""
    agent = ProjectAgent()
    return agent.list_projects()

def transfer_to_generator():
    return generator_agent

def transfer_to_updater():
    return updater_agent

def transfer_to_triage():
    return triage_agent

def read_project_files(project_name: str):
    """Read all files in a project for context."""
    processor = CodeProcessor()
    return processor.read_project_files(project_name)

def edit_file(project_name: str, file_path: str, content: str):
    """Edit a specific file in the project."""
    processor = CodeProcessor()
    return processor.edit_file(project_name, file_path, content)

def create_component(project_name: str, component_name: str, content: str):
    """Create a new React component."""
    processor = CodeProcessor()
    return processor.create_component(project_name, component_name, content)

def create_page(project_name: str, page_name: str, content: str):
    """Create a new Next.js page."""
    processor = CodeProcessor()
    return processor.create_page(project_name, page_name, content)

# Create specialized agents
generator_agent = Agent(
    name="NextJS Generator",
    instructions="""You are a NextJS website generator.
    - Help users create new NextJS websites based on their descriptions
    - Ask clarifying questions about design preferences and functionality
    - Generate appropriate components and pages
    - Use Tailwind CSS for styling
    - Implement responsive design
    - Follow NextJS best practices
    - After generation, suggest testing the site""",
    functions=[create_project, deploy_project, transfer_to_triage]
)

updater_agent = Agent(
    name="NextJS Updater",
    instructions="""You are a NextJS website updater.
    - Help users modify existing NextJS websites
    - Read and understand existing code
    - Create and modify components and pages
    - Update styles and functionality
    - Maintain code consistency
    - Test changes before deployment
    - Suggest improvements when appropriate
    
    You can:
    - Read project files for context
    - Edit existing files
    - Create new components
    - Create new pages
    - Deploy changes""",
    functions=[
        update_project,
        deploy_project,
        read_project_files,
        edit_file,
        create_component,
        create_page,
        transfer_to_triage
    ]
)

# Create the main triage agent
triage_agent = Agent(
    name="NextJS Project Manager",
    instructions="""You are a NextJS project management assistant.
    Determine which specialized agent should handle the user's request:
    - For creating new websites, transfer to the Generator Agent
    - For modifying existing sites, transfer to the Updater Agent
    - For listing projects, use current agent
    
    Common patterns to recognize:
    - "Create a website that..." -> Transfer to Generator Agent
    - "Make me a site for..." -> Transfer to Generator Agent
    - "Update the site to..." -> Transfer to Updater Agent
    - "Change the website..." -> Transfer to Updater Agent
    - "Show all projects" -> Use current agent
    - "List websites" -> Use current agent
    
    Ask clarifying questions if the user's intent is not clear.""",
    functions=[transfer_to_generator, transfer_to_updater, list_projects]
) 