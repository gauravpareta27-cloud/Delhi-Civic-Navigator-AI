from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag import rag_pipeline
from elastic import es_client

router = APIRouter()

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    response: str

@router.post("/api/search", response_model=SearchResponse)
async def search_services(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    try:
        answer = rag_pipeline.query(request.query)
        return SearchResponse(response=answer)
    except Exception as e:
        print(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")

@router.get("/api/health")
async def health_check():
    return {"status": "healthy", "documents_indexed": len(es_client.documents)}
