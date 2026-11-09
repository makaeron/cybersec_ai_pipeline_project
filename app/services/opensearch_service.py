from opensearchpy import OpenSearch  # OpenSearch client library.  

from app.config import settings  # Read app settings.  


class OpenSearchService:  # Helper for indexing searchable events.  
    def __init__(self) -> None:  # Create the search client.  
        self.client = OpenSearch(  # Build a simple OpenSearch client.  
            hosts=[{"host": settings.opensearch_host, "port": settings.opensearch_port}],  # Set host and port.  
            use_ssl=False,  # Keep local setup simple.  
            verify_certs=False,  # Skip certificate checks locally.  
        )  # Finish client setup.  

    def index_document(self, document_id: str, body: dict) -> None:  # Save one document into OpenSearch.  
        self.client.index(index=settings.opensearch_index, id=document_id, body=body)  # Write document to index.
