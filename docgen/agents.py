from typing import Optional
from datetime import datetime
from database import get_db_session, Document
from sqlalchemy import or_, func, distinct

class DocumentAgent:
    def __init__(self):
        self.db = get_db_session()

    def add_document(self, content: str, source: str) -> None:
        """Add a document to the PostgreSQL database."""
        try:
            doc = Document(
                content=content,
                doc_metadata={
                    "source": source,
                    "created_at": datetime.utcnow().isoformat()
                }
            )
            self.db.add(doc)
            self.db.commit()
            print(f"Successfully added document from {source}")
        except Exception as e:
            print(f"Error adding document: {str(e)}")
            self.db.rollback()

    def list_sources(self) -> list:
        """List all unique document sources in the database."""
        try:
            # Get unique URLs and their document counts
            sources = self.db.query(
                Document.url,
                func.count(Document.id).label('document_count'),
                func.min(Document.created_at).label('first_added')
            ).filter(
                Document.url.isnot(None)
            ).group_by(
                Document.url
            ).all()

            return [{
                'url': source.url,
                'document_count': source.document_count,
                'first_added': source.first_added.isoformat()
            } for source in sources]
        except Exception as e:
            print(f"Error listing sources: {str(e)}")
            return []

    def get_documents_by_url(self, url: str) -> list:
        """Get all documents from a specific URL."""
        try:
            docs = self.db.query(Document).filter(
                Document.url == url
            ).order_by(
                Document.created_at
            ).all()

            return [{
                'content': doc.content,
                'metadata': doc.doc_metadata,
                'created_at': doc.created_at.isoformat(),
                'title': doc.title,
                'description': doc.description
            } for doc in docs]
        except Exception as e:
            print(f"Error getting documents for URL {url}: {str(e)}")
            return []

    def search_documents(self, query: str, limit: int = 5) -> list:
        """Search for documents using PostgreSQL text search."""
        try:
            results = self.db.query(Document).filter(
                or_(
                    Document.content.ilike(f"%{query}%"),
                    Document.title.ilike(f"%{query}%"),
                    Document.description.ilike(f"%{query}%")
                )
            ).limit(limit).all()

            return [{
                'content': doc.content,
                'metadata': doc.doc_metadata,
                'score': 1.0,  # Simple relevance score
                'url': doc.url,
                'title': doc.title
            } for doc in results]
        except Exception as e:
            print(f"Error searching documents: {str(e)}")
            return []

    def __del__(self):
        """Cleanup when the agent is destroyed."""
        if hasattr(self, 'db'):
            self.db.close()

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
        print(f"\nFound document: {doc['content']}")
        print(f"Source: {doc['metadata']['source']}")