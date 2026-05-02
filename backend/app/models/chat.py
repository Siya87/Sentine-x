"""
Chat Assistant Models
Data models for AI-powered chat assistant
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message role in conversation"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Single chat message"""
    role: MessageRole = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "What is a phishing attack?",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class ChatSession(BaseModel):
    """Chat conversation session"""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    messages: List[ChatMessage] = Field(default_factory=list, description="Conversation messages")
    context: Dict[str, Any] = Field(default_factory=dict, description="Session context")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Session creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")
    is_active: bool = Field(True, description="Whether session is active")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "chat-session-123",
                "user_id": "user-456",
                "messages": [],
                "context": {},
                "created_at": "2024-01-15T10:00:00Z",
                "is_active": True
            }
        }


class ChatRequest(BaseModel):
    """Request to send a message to the chat assistant"""
    session_id: Optional[str] = Field(None, description="Existing session ID (optional)")
    message: str = Field(..., description="User message")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    use_knowledge_base: bool = Field(True, description="Use cybersecurity knowledge base")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "chat-session-123",
                "message": "What is the MITRE ATT&CK framework?",
                "use_knowledge_base": True
            }
        }


class ChatResponse(BaseModel):
    """Response from the chat assistant"""
    session_id: str = Field(..., description="Session identifier")
    message: ChatMessage = Field(..., description="Assistant's response message")
    suggestions: List[str] = Field(default_factory=list, description="Suggested follow-up questions")
    sources: List[str] = Field(default_factory=list, description="Information sources used")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Response confidence (0-1)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "chat-session-123",
                "message": {
                    "role": "assistant",
                    "content": "The MITRE ATT&CK framework is...",
                    "timestamp": "2024-01-15T10:30:05Z"
                },
                "suggestions": [
                    "Tell me about common attack techniques",
                    "How can I detect these attacks?"
                ],
                "confidence": 0.95
            }
        }


class ChatHistoryRequest(BaseModel):
    """Request to get chat history"""
    session_id: str = Field(..., description="Session identifier")
    limit: int = Field(50, ge=1, le=100, description="Maximum number of messages")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "chat-session-123",
                "limit": 50
            }
        }


class ChatSessionListResponse(BaseModel):
    """Response containing list of chat sessions"""
    sessions: List[ChatSession] = Field(..., description="List of chat sessions")
    total: int = Field(..., description="Total number of sessions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "sessions": [],
                "total": 5
            }
        }


class QuestionCategory(str, Enum):
    """Categories of cybersecurity questions"""
    THREAT_ANALYSIS = "threat_analysis"
    INCIDENT_RESPONSE = "incident_response"
    MITRE_ATTACK = "mitre_attack"
    MALWARE_ANALYSIS = "malware_analysis"
    PHISHING = "phishing"
    OSINT = "osint"
    GENERAL = "general"
    TOOLS = "tools"
    BEST_PRACTICES = "best_practices"


class KnowledgeBaseEntry(BaseModel):
    """Entry in the cybersecurity knowledge base"""
    id: str = Field(..., description="Entry identifier")
    category: QuestionCategory = Field(..., description="Question category")
    question: str = Field(..., description="Question or topic")
    answer: str = Field(..., description="Answer or explanation")
    keywords: List[str] = Field(default_factory=list, description="Related keywords")
    related_topics: List[str] = Field(default_factory=list, description="Related topics")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "kb-001",
                "category": "mitre_attack",
                "question": "What is MITRE ATT&CK?",
                "answer": "MITRE ATT&CK is a globally-accessible knowledge base...",
                "keywords": ["mitre", "attack", "framework", "tactics", "techniques"],
                "related_topics": ["threat intelligence", "incident response"]
            }
        }


class ChatAnalyticsRequest(BaseModel):
    """Request for chat analytics"""
    start_date: Optional[datetime] = Field(None, description="Start date for analytics")
    end_date: Optional[datetime] = Field(None, description="End date for analytics")
    
    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2024-01-01T00:00:00Z",
                "end_date": "2024-01-31T23:59:59Z"
            }
        }


class ChatAnalyticsResponse(BaseModel):
    """Chat analytics data"""
    total_sessions: int = Field(..., description="Total number of sessions")
    total_messages: int = Field(..., description="Total number of messages")
    avg_messages_per_session: float = Field(..., description="Average messages per session")
    top_categories: Dict[str, int] = Field(..., description="Top question categories")
    common_questions: List[str] = Field(..., description="Most common questions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_sessions": 150,
                "total_messages": 750,
                "avg_messages_per_session": 5.0,
                "top_categories": {
                    "threat_analysis": 45,
                    "phishing": 30,
                    "mitre_attack": 25
                },
                "common_questions": [
                    "What is phishing?",
                    "How to detect malware?",
                    "Explain MITRE ATT&CK"
                ]
            }
        }

# Made with Bob
