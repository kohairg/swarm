from firecrawl import FirecrawlApp
import os
from typing import List, Dict
from langchain_community.document_loaders import FireCrawlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from datetime import datetime
from database import get_db_session, Document
from sqlalchemy import or_

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env.local'))
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class DocumentProcessor:
    def __init__(self):
        self.chunk_size = int(os.getenv("CHUNK_SIZE", 1000))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 200))
        self.max_results = int(os.getenv("MAX_RESULTS", 5))
        
        # Initialize FireCrawl
        self.firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        
        # Get database session
        self.db = get_db_session()

    def _clean_metadata(self, metadata: Dict) -> Dict:
        """Clean and normalize metadata"""
        if not metadata:
            return {
                "source": "unknown",
                "created_at": datetime.utcnow().isoformat(),
                "title": "",
                "description": "",
                "language": "en",
                "url": ""
            }

        return {
            "source": metadata.get("source", metadata.get("url", "unknown")),
            "created_at": datetime.utcnow().isoformat(),
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "language": metadata.get("language", "en"),
            "url": metadata.get("url", "")
        }

    def crawl_and_store(self, url: str) -> List[Dict]:
        """Crawl a website and store content in PostgreSQL"""
        try:
            # Use FireCrawl to get content
            loader = FireCrawlLoader(
                api_key=os.getenv("FIRECRAWL_API_KEY"),
                url=url,
                mode="crawl"
            )
            docs = loader.load()
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(docs)
            
            # Store in PostgreSQL
            stored_chunks = []
            for chunk in chunks:
                try:
                    metadata = self._clean_metadata(chunk.metadata)
                    doc = Document(
                        content=chunk.page_content,
                        doc_metadata=metadata,
                        url=url,
                        title=metadata.get("title"),
                        description=metadata.get("description")
                    )
                    self.db.add(doc)
                    stored_chunks.append(chunk)
                except Exception as e:
                    print(f"Error storing chunk: {str(e)}")
                    continue
            
            self.db.commit()
            return stored_chunks
            
        except Exception as e:
            print(f"Error in crawl_and_store: {str(e)}")
            self.db.rollback()
            return []

    def search_documents(self, query: str) -> List[Dict]:
        """Search documents using PostgreSQL full-text search"""
        try:
            # Basic text search using ILIKE
            results = self.db.query(Document).filter(
                or_(
                    Document.content.ilike(f"%{query}%"),
                    Document.title.ilike(f"%{query}%"),
                    Document.description.ilike(f"%{query}%")
                )
            ).limit(self.max_results).all()

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
        """Cleanup database session"""
        if hasattr(self, 'db'):
            self.db.close()