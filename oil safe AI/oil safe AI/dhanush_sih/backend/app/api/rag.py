from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import KnowledgeDocument
from app.schemas.schemas import RAGQueryRequest
from app.rag.knowledge_base import rag_knowledge_base

router = APIRouter(prefix="/rag", tags=["RAG & Knowledge Base"])

@router.get("/documents")
def get_knowledge_documents(db: Session = Depends(get_db)):
    return db.query(KnowledgeDocument).all()

@router.post("/query")
def query_rag_knowledge(req: RAGQueryRequest):
    results = rag_knowledge_base.search(req.query, top_k=req.top_k)
    return {
        "query": req.query,
        "results": results,
        "total_matches": len(results)
    }
