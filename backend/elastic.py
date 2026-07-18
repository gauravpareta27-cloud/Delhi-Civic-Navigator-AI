import json
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class ElasticsearchClient:
    """
    Official Elasticsearch integration for the Delhi Civic Navigator AI.
    Connects to a real Elasticsearch instance.
    """
    def __init__(self):
        # Connect to Elasticsearch (local by default, or via URL)
        es_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
        self.es = Elasticsearch(es_url)
        self.index_name = "delhi_services"

    def load_and_index(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file not found: {filepath}")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            documents = json.load(f)
            
        # Create index if it doesn't exist
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(
                index=self.index_name,
                body={
                    "mappings": {
                        "properties": {
                            "service_name": {"type": "text", "boost": 3},
                            "department": {"type": "text"},
                            "eligibility": {"type": "text"},
                            "required_documents": {"type": "text"},
                            "fees": {"type": "text"},
                            "processing_time": {"type": "text"},
                            "how_to_apply": {"type": "text"},
                            "official_source": {"type": "keyword"}
                        }
                    }
                }
            )
            print(f"Created index '{self.index_name}'.")

        # Prepare bulk index actions
        actions = [
            {
                "_index": self.index_name,
                "_id": idx,
                "_source": doc
            }
            for idx, doc in enumerate(documents)
        ]
        
        # Perform bulk indexing
        success, _ = bulk(self.es, actions)
        print(f"Successfully indexed {success} documents into Elasticsearch.")
        
        # Force a refresh to make documents immediately searchable
        self.es.indices.refresh(index=self.index_name)

    def search(self, query, top_k=1):
        """
        Search Elasticsearch using a multi-match query.
        """
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "service_name^3", 
                        "department^2", 
                        "eligibility", 
                        "required_documents", 
                        "how_to_apply"
                    ],
                    "fuzziness": "AUTO"
                }
            },
            "size": top_k
        }
        
        try:
            response = self.es.search(index=self.index_name, body=search_body)
            hits = response["hits"]["hits"]
            
            results = []
            for hit in hits:
                results.append(hit["_source"])
                
            return results
        except Exception as e:
            print(f"Elasticsearch search failed: {e}")
            return []

# Singleton instance to be used across the app
es_client = ElasticsearchClient()
