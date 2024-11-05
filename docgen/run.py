from swarm import Agent
from agents import DocumentAgent
from document_processor import DocumentProcessor

def add_document(content: str, source: str):
    """Add a document to the knowledge base."""
    agent = DocumentAgent()
    agent.add_document(content=content, source=source)
    return {"response": f"Document from {source} has been added successfully."}

def search_documents(query: str):
    """Search for documents using a text query."""
    agent = DocumentAgent()
    results = agent.search_documents(query)
    
    if not results:
        return {"response": "No relevant documents found."}
    
    formatted_results = []
    for doc in results:
        content = doc.properties['content']
        source = doc.properties['metadata']['source']
        formatted_results.append(f"\nSource: {source}\nContent: {content}")
    
    return {"response": "\n---\n".join(formatted_results)}

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

# Create specialized agents
search_agent = Agent(
    name="Search Agent",
    instructions="""You are a search specialist that helps users find documents.
    - Help users formulate effective search queries
    - Present results in a clear format
    - Ask clarifying questions if the search query is too vague""",
    functions=[search_documents, transfer_to_triage]
)

crawler_agent = Agent(
    name="Crawler Agent",
    instructions="""You are a web crawler specialist that helps users add documents.
    - Help users crawl websites and store content
    - Ask for the website URL if not provided
    - Verify the URL format before crawling
    - Make sure URLs start with http:// or https://
    - Warn users that crawling may take a few minutes for large sites""",
    functions=[crawl_website, transfer_to_triage]
)

# Create the main triage agent
triage_agent = Agent(
    name="Document Management Agent",
    instructions="""You are a document management assistant that helps users manage their documents.
    Determine which specialized agent should handle the user's request:
    - For searching existing documents, transfer to the Search Agent
    - For crawling websites and adding new content, transfer to the Crawler Agent
    
    Ask clarifying questions if the user's intent is not clear.""",
    functions=[transfer_to_search, transfer_to_crawler]
)

# Export the triage agent as the main interface
doc_agent = triage_agent

if __name__ == "__main__":
    from swarm.repl import run_demo_loop
    run_demo_loop(triage_agent)