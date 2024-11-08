# Document Generation Agent

A Swarm-based document management system that crawls websites, stores content in PostgreSQL, and provides intelligent search capabilities through specialized agents.

## System Architecture

### Core Components

1. **Document Processor** (`document_processor.py`)
   - Handles website crawling using FireCrawl
   - Chunks documents for efficient storage
   - Manages metadata cleaning and normalization
   - Interfaces with PostgreSQL for storage and retrieval
   - Key methods:
     - `crawl_and_store(url)`: Crawls websites and stores content
     - `search_documents(query)`: Searches stored documents
     - `_clean_metadata(metadata)`: Normalizes metadata fields

2. **Database** (`database.py`)
   - Manages PostgreSQL schema and connections
   - Handles document storage and retrieval
   - Provides full-text search capabilities
   - Schema:
     - `content`: Document content
     - `doc_metadata`: JSON metadata
     - `created_at`: Timestamp
     - `url`: Source URL
     - `title`: Document title
     - `description`: Document description

3. **Agents** (`agents.py`)
   - `DocumentAgent`: Base agent for document operations
   - Provides direct interface to PostgreSQL
   - Handles document addition and search
   - Methods:
     - `add_document(content, source)`: Adds single documents
     - `search_documents(query, limit)`: Performs text search

4. **Specialized Agents** (`run.py`)
   - `search_agent`: Handles document search requests
   - `crawler_agent`: Manages website crawling
   - `triage_agent`: Routes requests to appropriate agents
   - Functions:
     - `crawl_website(url)`: Initiates website crawling
     - `search_documents(query)`: Performs document search
     - `add_document(content, source)`: Adds individual documents

### Data Flow

1. **Document Ingestion**
   ```
   User Request → Triage Agent → Crawler Agent → Document Processor 
   → FireCrawl → Text Splitting → Metadata Cleaning → PostgreSQL Storage
   ```

2. **Document Search**
   ```
   User Query → Triage Agent → Search Agent → Document Agent 
   → PostgreSQL Query → Results Formatting → User Response
   ```

## Setup and Configuration

### Prerequisites
- Docker and Docker Compose
- Python 3.10+
- Make (optional, but recommended)
- PostgreSQL 15+

### Environment Variables
Create `.env.local` with:
```
OPENAI_API_KEY=your_openai_key
FIRECRAWL_API_KEY=your_firecrawl_key
DATABASE_URL=postgresql://docgen:docgen@localhost:5432/docgen
CHUNK_SIZE=1000           # Size of document chunks
CHUNK_OVERLAP=200         # Overlap between chunks
MAX_RESULTS=5             # Maximum search results
```

### Installation Steps

1. **Install Dependencies**
   ```bash
   make install
   ```

2. **Start PostgreSQL**
   ```bash
   make start
   ```

3. **Initialize Database**
   ```bash
   make setup
   ```

4. **Run the Agent**
   ```bash
   make run
   ```

## Usage Examples

### Crawling Websites
```
> Please crawl https://example.com
> Crawl the documentation at https://docs.example.com
```

### Searching Documents
```
> What do the docs say about authentication?
> Find information about API rate limits
> Search for configuration options
```

### Adding Individual Documents
```
> Add this document: "API rate limits are 100 requests per minute" from source "api_docs.txt"
```

## Database Schema

Documents are stored with the following structure:
- `id`: Primary key
- `content`: Document content (Text)
- `doc_metadata`: JSON metadata including:
  - `source`: Document source/URL
  - `created_at`: Timestamp
  - `language`: Content language
  - `url`: Source URL
- `created_at`: Creation timestamp
- `url`: Source URL
- `title`: Document title
- `description`: Document description

## Development

### Project Structure
```
docgen/
├── __init__.py           # Package marker
├── agents.py             # Agent implementations
├── database.py           # Database setup and models
├── document_processor.py # Core processing logic
├── run.py               # Main entry point
├── requirements.txt     # Dependencies
└── docker-compose.yml   # Container config
```

### Adding New Features
1. Update schema in `database.py`
2. Implement processing in `document_processor.py`
3. Add agent capabilities in `agents.py`
4. Update agent functions in `run.py`

### Testing
```bash
pytest docgen/evals.py
```

## Maintenance

### Docker Commands
- Start: `make start`
- Stop: `make stop`
- Logs: `make logs`
- Clean: `make clean`

### Common Issues
- Port conflicts: Check with `make check-ports`
- Database connection: Ensure PostgreSQL is running
- Search issues: Check PostgreSQL logs

## Dependencies

### Core
- `openai`: LLM capabilities
- `psycopg2-binary`: PostgreSQL driver
- `sqlalchemy`: Database ORM
- `firecrawl-py`: Web crawling
- `langchain`: Document processing

### Development
- `pytest`: Testing
- `docker`: Container management
- `make`: Build automation

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
MIT License