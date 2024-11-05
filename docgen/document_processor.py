from firecrawl import FirecrawlApp
import weaviate
import os
from typing import List, Dict
from langchain_community.document_loaders import FireCrawlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import re
from datetime import datetime

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env.local'))
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))  # fallback to .env

class DocumentProcessor:
    def __init__(self):
        # Load configuration from environment
        self.chunk_size = int(os.getenv("CHUNK_SIZE", 1000))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 200))
        self.max_results = int(os.getenv("MAX_RESULTS", 5))

        # Initialize clients
        self.firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
        
        # Use local Weaviate instance
        self.client = weaviate.WeaviateClient(
            connection_params=weaviate.connect.ConnectionParams.from_url(
                url="http://localhost:8080",
                grpc_port=50051
            )
        )
        self.client.connect()
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def _clean_metadata(self, metadata: Dict) -> Dict:
        """Clean metadata to conform to Weaviate's property name requirements."""
        # Initialize with default values
        cleaned = {
            "source": "unknown",
            "created_at": datetime.now().isoformat(),
            "title": "",
            "description": "",
            "language": "en",
            "url": "",
            "og_title": "",
            "og_description": "",
            "og_image": "",
            "twitter_card": "",
            "twitter_image": ""
        }
        
        if not metadata:
            return cleaned

        # Helper function to safely get nested values
        def safe_get(d: Dict, *keys, default=""):
            for key in keys:
                if not isinstance(d, dict):
                    return default
                d = d.get(key, default)
            return d if d is not None else default

        # Update with available metadata
        try:
            cleaned.update({
                "source": safe_get(metadata, "source", default=metadata.get("url", "unknown")),
                "created_at": datetime.now().isoformat(),
                "title": safe_get(metadata, "title"),
                "description": safe_get(metadata, "description"),
                "language": safe_get(metadata, "language", default="en"),
                "url": safe_get(metadata, "url"),
                "og_title": safe_get(metadata, "og:title", "og_title"),
                "og_description": safe_get(metadata, "og:description", "og_description"),
                "og_image": safe_get(metadata, "og:image", "og_image"),
                "twitter_card": safe_get(metadata, "twitter:card", "twitter_card"),
                "twitter_image": safe_get(metadata, "twitter:image", "twitter_image")
            })
        except Exception as e:
            print(f"Error cleaning metadata: {str(e)}")
            # Return default metadata if cleaning fails
            return cleaned

        return cleaned

    def crawl_and_store(self, url: str) -> List[Dict]:
        """Crawl a website and store the content in Weaviate"""
        try:
            # Use Firecrawl to get website content
            loader = FireCrawlLoader(
                api_key=os.getenv("FIRECRAWL_API_KEY"),
                url=url,
                mode="crawl"
            )
            docs = loader.load()
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(docs)
            
            # Store in Weaviate
            stored_chunks = []
            for chunk in chunks:
                try:
                    # Ensure chunk has metadata
                    if not hasattr(chunk, 'metadata'):
                        chunk.metadata = {}
                    
                    # Add URL to metadata if not present
                    if 'url' not in chunk.metadata:
                        chunk.metadata['url'] = url
                    
                    # Clean metadata
                    cleaned_metadata = self._clean_metadata(chunk.metadata)
                    
                    # Store in Weaviate
                    self.client.collections.get("Document").data.insert({
                        "content": chunk.page_content,
                        "metadata": cleaned_metadata
                    })
                    stored_chunks.append(chunk)
                except Exception as e:
                    print(f"Error storing chunk: {str(e)}")
                    continue
            
            return stored_chunks
        except Exception as e:
            print(f"Error in crawl_and_store: {str(e)}")
            return []

    def query_documents(self, query: str) -> List[Dict]:
        """Query the Weaviate database"""
        try:
            response = (
                self.client.query
                .get("Document", ["content", "metadata", "url"])
                .with_near_text({"concepts": [query]})
                .with_limit(self.max_results)
                .do()
            )
            return response["data"]["Get"]["Document"]
        except Exception as e:
            print(f"Error querying documents: {str(e)}")
            return []

    def __del__(self):
        """Cleanup when the processor is destroyed."""
        if hasattr(self, 'client'):
            self.client.close()