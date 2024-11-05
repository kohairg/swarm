from typing import Optional
import weaviate
from weaviate import WeaviateClient
from datetime import datetime

class DocumentAgent:
    def __init__(self):
        self.client = WeaviateClient(
            connection_params=weaviate.connect.ConnectionParams.from_url(
                url="http://localhost:8080",
                grpc_port=50051
            )
        )
        self.client.connect()

    def add_document(self, content: str, source: str) -> None:
        """Add a document to the Weaviate collection."""
        try:
            self.client.collections.get("Document").data.insert({
                "content": content,
                "metadata": {
                    "source": source,
                    "created_at": datetime.now().isoformat()
                }
            })
            print(f"Successfully added document from {source}")
        except Exception as e:
            print(f"Error adding document: {str(e)}")

    def search_documents(self, query: str, limit: int = 5) -> list:
        """Search for documents using a text query."""
        try:
            result = (
                self.client.collections.get("Document")
                .query.bm25(
                    query=query,
                    properties=["content"]
                )
                .with_limit(limit)
                .with_additional(["distance"])
                .do()
            )
            return result.objects
        except Exception as e:
            print(f"Error searching documents: {str(e)}")
            return []

    def __del__(self):
        """Cleanup when the agent is destroyed."""
        if hasattr(self, 'client'):
            self.client.close()

# Example usage
if __name__ == "__main__":
    agent = DocumentAgent()
    
    # Example: Add a document
    agent.add_document(
        content="This is a test document about Python programming.",
        source="test.txt"
    )
    
    # Example: Search documents
    results = agent.search_documents("Python")
    for doc in results:
        print(f"\nFound document: {doc.properties['content']}")
        print(f"Source: {doc.properties['metadata']['source']}") 