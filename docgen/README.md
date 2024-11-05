# Document Generation Agent

This example is a Swarm containing a document generation agent that can crawl websites, store content in a Weaviate database, and answer questions based on the stored content.

## Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Make (optional, but recommended)

## Setup

1. Install dependencies:
```bash
make install
# or
pip install -r requirements.txt
```

2. Set up environment variables:
   - Copy `.env.example` to `.env.local`
   ```bash
   cp .env.example .env.local
   ```
   - Edit `.env.local` with your API keys
   ```bash
   vim .env.local  # or use your preferred editor
   ```

3. Start Weaviate and initialize schema:
```bash
make setup
# or
docker-compose up -d
python setup_weaviate.py
```

4. Run the agent:
```bash
make run
# or
python -m docgen.run
```

## Docker Commands

- Start Weaviate: `make start` or `docker-compose up -d`
- Stop Weaviate: `make stop` or `docker-compose down`
- View logs: `make logs` or `docker-compose logs -f weaviate`
- Clean up (including volumes): `make clean` or `docker-compose down -v`

## Environment Variables

The following environment variables can be configured in `.env.local`:

- `OPENAI_API_KEY`: Your OpenAI API key
- `FIRECRAWL_API_KEY`: Your Firecrawl API key
- `CHUNK_SIZE`: Size of document chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `MAX_RESULTS`: Maximum number of search results (default: 5)

## Usage

The agent can:
- Crawl websites and store content: "Please crawl https://example.com"
- Search stored documents: "What do the docs say about X?"
- Handle refunds and sales inquiries

## Evals

To run the tests:
```bash
pytest docgen/evals.py
```