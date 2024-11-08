from swarm import Agent
from agents import DocumentAgent
from document_processor import DocumentProcessor

def add_document(content: str, source: str):
    """Add a document to the knowledge base."""
    agent = DocumentAgent()
    agent.add_document(content=content, source=source)
    return {"response": f"Document from {source} has been added successfully."}

def search_documents(query: str):
    """Search for documents using text search."""
    agent = DocumentAgent()
    results = agent.search_documents(query)
    
    if not results:
        return {"response": "No relevant documents found."}
    
    formatted_results = []
    for doc in results:
        content = doc['content']
        metadata = doc['metadata']
        score = doc['score']
        
        # Format source information
        source_info = f"Source: {metadata['source']}"
        if doc.get('title'):
            source_info += f" - {doc['title']}"
        
        # Format the result with relevance score
        formatted_results.append(
            f"\n{source_info}\nRelevance: {score:.2f}\nContent: {content}"
        )
    
    # Add a summary of the search
    summary = f"Found {len(formatted_results)} relevant documents. Here are the most relevant excerpts:"
    
    return {"response": f"{summary}\n\n{'---'.join(formatted_results)}"}

def crawl_website(url: str):
    """Crawl a website and store its content in the knowledge base."""
    try:
        processor = DocumentProcessor()
        chunks = processor.crawl_and_store(url)
        
        # Format response with summary of what was stored
        num_chunks = len(chunks)
        response = f"Successfully crawled {url} and stored {num_chunks} document chunks.\n"
        
        # Add sample of first chunk if available
        if chunks:
            first_chunk = chunks[0]
            response += f"\nSample content from first chunk:\n{first_chunk.page_content[:200]}..."
            
        return {"response": response}
    except Exception as e:
        return {"response": f"Error crawling website: {str(e)}"}

def transfer_to_search():
    """Transfer to search agent when user wants to search documents."""
    return search_agent

def transfer_to_crawler():
    """Transfer to crawler agent when user wants to crawl websites."""
    return crawler_agent

def transfer_to_triage():
    """Transfer back to triage agent."""
    return triage_agent

def list_sources():
    """List all crawled websites and document sources."""
    agent = DocumentAgent()
    sources = agent.list_sources()
    
    if not sources:
        return {"response": "No documents have been stored yet."}
    
    # Format the response
    formatted_sources = []
    for source in sources:
        formatted_sources.append(
            f"\nSource: {source['url']}\n"
            f"Documents: {source['document_count']}\n"
            f"First Added: {source['first_added']}"
        )
    
    summary = f"Found {len(formatted_sources)} unique sources:"
    return {"response": f"{summary}\n{'---'.join(formatted_sources)}"}

def list_documents_by_url(url: str):
    """List all documents from a specific URL."""
    agent = DocumentAgent()
    documents = agent.get_documents_by_url(url)
    
    if not documents:
        return {"response": f"No documents found for URL: {url}"}
    
    # Format the response
    formatted_docs = []
    for i, doc in enumerate(documents, 1):
        formatted_docs.append(
            f"\nDocument {i}:\n"
            f"Title: {doc['title'] or 'No title'}\n"
            f"Created: {doc['created_at']}\n"
            f"Content Preview: {doc['content'][:200]}..."
        )
    
    summary = f"Found {len(formatted_docs)} documents from {url}:"
    return {"response": f"{summary}\n{'---'.join(formatted_docs)}"}

# Create specialized agents
search_agent = Agent(
    name="Search Agent",
    instructions="""You are a search specialist that helps users find documents.
    - Help users formulate effective search queries
    - Present results in a clear format
    - Include context from the document metadata when available
    - Ask clarifying questions if the search query is too vague
    - If no results are found, suggest alternative search terms
    - You can search through all stored documents using the search_documents function
    - You can list all sources using the list_sources function
    - You can show all documents from a specific site using list_documents_by_url
    - Always search when users ask about specific information""",
    functions=[search_documents, list_sources, list_documents_by_url, transfer_to_triage]
)

crawler_agent = Agent(
    name="Crawler Agent",
    instructions="""You are a web crawler specialist that helps users add documents.
    - Help users crawl websites and store content
    - Ask for the website URL if not provided
    - Verify the URL format before crawling
    - Make sure URLs start with http:// or https://
    - Warn users that crawling may take a few minutes for large sites
    - After crawling, suggest searching the content
    - You can show all crawled sites using list_sources
    - You can show all documents from a site using list_documents_by_url
    - After crawling, show the documents that were stored""",
    functions=[crawl_website, list_sources, list_documents_by_url, transfer_to_triage]
)

# Create the main triage agent
triage_agent = Agent(
    name="Document Management Agent",
    instructions="""You are a document management assistant that helps users manage their documents.
    Determine which specialized agent should handle the user's request:
    - For searching existing documents, transfer to the Search Agent
    - For crawling websites and adding new content, transfer to the Crawler Agent
    - For listing all sources or documents, use either agent
    
    Common patterns to recognize:
    - "What does X say about Y?" -> Transfer to Search Agent
    - "Find information about X" -> Transfer to Search Agent
    - "Search for X" -> Transfer to Search Agent
    - "Crawl website X" -> Transfer to Crawler Agent
    - "Add content from X" -> Transfer to Crawler Agent
    - "Show all sources" -> Use current agent
    - "List crawled sites" -> Use current agent
    - "Show documents from X" -> Use current agent
    
    Ask clarifying questions if the user's intent is not clear.""",
    functions=[transfer_to_search, transfer_to_crawler, list_sources, list_documents_by_url]
)

# Export the triage agent as the main interface
doc_agent = triage_agent

if __name__ == "__main__":
    from swarm.repl import run_demo_loop
    run_demo_loop(triage_agent)