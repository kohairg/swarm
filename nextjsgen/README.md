# NextJS Generation Agent

A Swarm-based NextJS website generation system that creates, modifies, and deploys NextJS applications based on natural language descriptions.

## System Architecture

### Core Components

1. **Project Generator** (`agents.py`)
   - Creates new NextJS projects
   - Manages project structure and files
   - Handles component generation
   - Interfaces with PostgreSQL for project tracking
   - Key methods:
     - `create_project(name, description)`: Creates new projects
     - `update_project(name, changes)`: Updates existing projects
     - `deploy_project(name)`: Deploys projects locally

2. **Database** (`database.py`)
   - Manages PostgreSQL schema and connections
   - Tracks project metadata and configuration
   - Schema:
     - `name`: Project name
     - `description`: Project description
     - `created_at`: Creation timestamp
     - `updated_at`: Last update timestamp
     - `project_path`: Local filesystem path
     - `config`: Project configuration
     - `components`: Component metadata
     - `pages`: Page structure
     - `dependencies`: Project dependencies

3. **Specialized Agents** (`run.py`)
   - `generator_agent`: Creates new websites
   - `updater_agent`: Modifies existing sites
   - `triage_agent`: Routes requests to appropriate agents

## Setup

1. Install dependencies: 