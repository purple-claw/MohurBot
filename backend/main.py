from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import logging
import os
from pathlib import Path

from knowledgeBase import find_best_match
from chatHis import add_entry, load_history, clear_history, get_history_count
from llm_service import llm_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mohur AI Chatbot API", version="2.0")

# Adding the Universally Peice of Trash ---  CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for containerized deployment
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    status: str
    source: str 

class HistoryResponse(BaseModel):
    history: List[Dict[str, Any]]
    count: int

@app.post("/api/ask", response_model=AnswerResponse)
async def handle_question(request: QuestionRequest):
    try:
        question = request.question.strip() 
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        logger.info(f"Processing your question: {question}")
        logger.info(f"Request from client received successfully")
        
        # First, I will check knowledge base for relevant context
        kb_result = find_best_match(question)
        logger.info(f"KB match result: confidence={kb_result['confidence']}, matched={kb_result['matched']}")
        
        # Use LLM service to generate enhanced response
        try:
            # If knowledge base has good match, I will for sure use it as context
            if kb_result['matched'] and kb_result['confidence'] >= 4:
                llm_answer = llm_service.get_response(question, context=kb_result['answer'])
                source = "llm_with_kb"
                answer = llm_answer
                logger.info(f"Using KB context with AI enhancement")
            else:
                # If not then I will Use LLM without knowledge base context
                llm_answer = llm_service.get_response(question)
                source = "llm_only"
                answer = llm_answer
                logger.info(f"Using AI only - KB confidence too low")
                
        except Exception as llm_error:
            logger.error(f"LLM service error: {llm_error}")
            # Fallback to knowledge base only if available
            if kb_result['matched']:
                answer = kb_result['answer']
                source = "kb_fallback"
            else:
                answer = "I'm having trouble processing your question right now. Could you please try rephrasing it or ask about productivity, remote work, or professional development topics?"
                source = "error_fallback"
        
        # Hehe now add this to history
        add_entry(question, answer, source)
        
        logger.info(f"Response generated using: {source}")
        
        return AnswerResponse(
            question=question,
            answer=answer,
            status="success",
            source=source
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history", response_model=HistoryResponse)
async def get_history():
    try:
        history = load_history()
        return HistoryResponse(
            history=history,
            count=len(history)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint and logic to delete the chat history, like your chrome Browsing History Hehehehe...
@app.delete("/api/history")
async def clear_chat_history():
    try:
        success = clear_history()
        if success:
            logger.info("Chat history cleared successfully")
            return {
                "status": "success", 
                "message": "Chat history cleared successfully",
                "count": 0
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to clear chat history")
    except Exception as e:
        logger.error(f"Error clearing chat history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# End point to check the servers health,,,, Even servers sometimes get fever....
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "2.0", "features": ["llm_integration", "enhanced_responses", "cors_enabled"]}

# Testing our Universal Troublesome Peice of SHit,,, The CORS
@app.get("/api/test-cors")
async def test_cors():
    return {"message": "CORS is working!", "timestamp": "2025-10-01", "status": "success"}


# If the Knowledege Base Responses are ugly as you, then enhance it using GPT
@app.post("/api/enhance")
async def enhance_response(request: QuestionRequest):
    try:
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Text to enhance is required")
        
        enhanced = llm_service.enhance_fallback_response(question, "enhance this text")
        return {"original": question, "enhanced": enhanced, "status": "success"}
        
    except Exception as e:
        logger.error(f"Error enhancing text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Getting the stats, see how much you used it, like your brain
@app.get("/api/stats")
async def get_stats():
    """
    Get chatbot statistics
    """
    try:
        history = load_history()
        total_conversations = len(history)
        
        # Count different response sources if available
        llm_responses = sum(1 for entry in history if entry.get('source') in ['llm_with_kb', 'llm_only'])
        kb_responses = sum(1 for entry in history if entry.get('source') == 'kb_fallback')
        
        return {
            "total_conversations": total_conversations,
            "llm_enhanced_responses": llm_responses,
            "knowledge_base_responses": kb_responses,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files for frontend
static_dir = Path(__file__).parent.parent / "frontend" / "build"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir / "static")), name="static")
    
    @app.get("/")
    async def serve_frontend():
        return FileResponse(str(static_dir / "index.html"))
    
    @app.get("/{full_path:path}")
    async def serve_frontend_routes(full_path: str):
        # Skip API routes
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")
            
        # Serve static files
        file_path = static_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        # For all other routes, serve index.html (SPA routing)
        return FileResponse(str(static_dir / "index.html"))

# Export the app for deployment
handler = app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)