"""
Chat Assistant API Routes
Endpoints for AI-powered conversational assistant
"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional
import logging

from app.models.chat import (
    ChatRequest, ChatResponse, ChatHistoryRequest,
    ChatSessionListResponse, ChatAnalyticsRequest, ChatAnalyticsResponse
)
from app.services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter()
chat_service = ChatService()


@router.post("/message", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_message(request: ChatRequest):
    """
    Send a message to the AI chat assistant
    
    The assistant can answer questions about:
    - Cybersecurity concepts and threats
    - MITRE ATT&CK framework
    - Phishing and social engineering
    - Malware analysis
    - Incident response
    - OSINT techniques
    - Security best practices
    - Security tools and technologies
    
    The assistant maintains conversation context and provides relevant suggestions.
    """
    try:
        logger.info(f"Processing chat message: {request.message[:50]}...")
        response = await chat_service.send_message(request)
        return response
    except Exception as e:
        logger.error(f"Failed to process chat message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


@router.get("/session/{session_id}", response_model=ChatResponse)
async def get_session_history(session_id: str, limit: int = 50):
    """
    Get chat session history
    
    Retrieves the conversation history for a specific session,
    including all messages exchanged between the user and assistant.
    """
    try:
        logger.info(f"Retrieving session history: {session_id}")
        session = await chat_service.get_session(session_id)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {session_id} not found"
            )
        
        # Return last message as response with full history in session
        if session.messages:
            last_message = session.messages[-1]
            return ChatResponse(
                session_id=session.session_id,
                message=last_message,
                suggestions=[],
                sources=[],
                confidence=None
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No messages in session"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve session {session_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve session: {str(e)}"
        )


@router.get("/sessions", response_model=ChatSessionListResponse)
async def list_sessions(user_id: Optional[str] = None, limit: int = 10):
    """
    List chat sessions
    
    Returns a list of chat sessions, optionally filtered by user ID.
    Sessions are sorted by last update time (most recent first).
    """
    try:
        logger.info(f"Listing chat sessions (user_id={user_id}, limit={limit})")
        sessions = await chat_service.list_sessions(user_id=user_id, limit=limit)
        return sessions
    except Exception as e:
        logger.error(f"Failed to list sessions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {str(e)}"
        )


@router.delete("/session/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str):
    """
    Delete a chat session
    
    Marks a chat session as inactive. The session data is retained
    but will not appear in active session lists.
    """
    try:
        logger.info(f"Deleting session: {session_id}")
        success = await chat_service.delete_session(session_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {session_id} not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete session {session_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}"
        )


@router.post("/analytics", response_model=ChatAnalyticsResponse)
async def get_analytics(request: ChatAnalyticsRequest):
    """
    Get chat analytics
    
    Returns analytics data including:
    - Total number of sessions and messages
    - Average messages per session
    - Top question categories
    - Most common questions
    
    Can be filtered by date range.
    """
    try:
        logger.info("Fetching chat analytics")
        analytics = await chat_service.get_analytics(
            start_date=request.start_date,
            end_date=request.end_date
        )
        return analytics
    except Exception as e:
        logger.error(f"Failed to get analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analytics: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for chat service
    
    Returns the status of the chat assistant service and
    information about the knowledge base.
    """
    try:
        kb_size = len(chat_service.knowledge_base)
        return {
            "status": "healthy",
            "service": "Chat Assistant",
            "knowledge_base_entries": kb_size,
            "ai_model": "IBM Granite" if chat_service.ai_service.model else "Mock Mode"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        )


@router.get("/knowledge-base")
async def get_knowledge_base():
    """
    Get cybersecurity knowledge base
    
    Returns all entries in the cybersecurity knowledge base
    that the chat assistant uses to answer questions.
    """
    try:
        logger.info("Retrieving knowledge base")
        kb_entries = [entry.model_dump() for entry in chat_service.knowledge_base]
        return {
            "total_entries": len(kb_entries),
            "entries": kb_entries
        }
    except Exception as e:
        logger.error(f"Failed to retrieve knowledge base: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve knowledge base: {str(e)}"
        )

# Made with Bob
