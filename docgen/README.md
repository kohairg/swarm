# Document Generation Agent

A Swarm-based document management system that crawls websites, stores content in Weaviate, and provides intelligent search capabilities through specialized agents.

## System Architecture

### Core Components

1. **Document Processor** (`document_processor.py`)
   - Handles website crawling using FireCrawl
   - Chunks documents for efficient storage
   - Manages metadata cleaning and normalization
   - Interfaces with Weaviate for storage and retrieval
   - Key methods:
     - `crawl_and_store(url)`: Crawls websites and stores content
     - `query_documents(query)`: Searches stored documents
     - `_clean_metadata(metadata)`: Normalizes metadata fields

2. **Agents** (`agents.py`)
   - `DocumentAgent`: Base agent for document operations
   - Provides direct interface to Weaviate
   - Handles document addition and search
   - Methods:
     - `add_document(content, source)`: Adds single documents
     - `search_documents(query, limit)`: Performs BM25 search

3. **Specialized Agents** (`run.py`)
   - `search_agent`: Handles document search requests
   - `crawler_agent`: Manages website crawling
   - `triage_agent`: Routes requests to appropriate agents
   - Functions:
     - `crawl_website(url)`: Initiates website crawling
     - `search_documents(query)`: Performs document search
     - `add_document(content, source)`: Adds individual documents

4. **Weaviate Setup** (`setup_weaviate.py`)
   - Configures Weaviate schema
   - Defines document properties and metadata structure
   - Handles collection creation and cleanup

### Data Flow

1. **Document Ingestion**
   ```
   User Request → Triage Agent → Crawler Agent → Document Processor 
   → FireCrawl → Text Splitting → Metadata Cleaning → Weaviate Storage
   ```

2. **Document Search**
   ```
   User Query → Triage Agent → Search Agent → Document Agent 
   → Weaviate Query → Results Formatting → User Response
   ```

## Setup and Configuration

### Prerequisites
- Docker and Docker Compose
- Python 3.10+
- Make (optional, but recommended)

### Environment Variables
Create `.env.local` with: