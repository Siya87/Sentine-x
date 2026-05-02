"""
Chat Assistant Service
AI-powered conversational assistant for cybersecurity questions
"""
import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import uuid
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.chat import (
    ChatSession, ChatMessage, ChatRequest, ChatResponse,
    MessageRole, QuestionCategory, KnowledgeBaseEntry,
    ChatSessionListResponse, ChatAnalyticsResponse
)
from app.services.ai_service import AIService
from app.database.mongodb import get_database

logger = logging.getLogger(__name__)


class ChatService:
    """Service for AI-powered chat assistant"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.sessions_collection = "chat_sessions"
        self.knowledge_base = self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self) -> List[KnowledgeBaseEntry]:
        """Initialize cybersecurity knowledge base"""
        return [
            KnowledgeBaseEntry(
                id="kb-001",
                category=QuestionCategory.MITRE_ATTACK,
                question="What is MITRE ATT&CK?",
                answer="MITRE ATT&CK is a globally-accessible knowledge base of adversary tactics and techniques based on real-world observations. It provides a common language for describing cyber attacks and helps organizations understand their security posture.",
                keywords=["mitre", "attack", "framework", "tactics", "techniques"],
                related_topics=["threat intelligence", "incident response", "security assessment"]
            ),
            KnowledgeBaseEntry(
                id="kb-002",
                category=QuestionCategory.PHISHING,
                question="What is phishing?",
                answer="Phishing is a cyber attack that uses disguised email, text messages, or websites to trick people into providing sensitive information, downloading malware, or taking actions that compromise security. Common indicators include urgency, suspicious links, and requests for credentials.",
                keywords=["phishing", "social engineering", "email", "credentials"],
                related_topics=["spear phishing", "whaling", "email security"]
            ),
            KnowledgeBaseEntry(
                id="kb-003",
                category=QuestionCategory.MALWARE_ANALYSIS,
                question="What is ransomware?",
                answer="Ransomware is malicious software that encrypts files or locks systems, demanding payment for decryption. It typically spreads through phishing emails, exploit kits, or compromised credentials. Prevention includes regular backups, security updates, and user training.",
                keywords=["ransomware", "malware", "encryption", "extortion"],
                related_topics=["backup strategies", "incident response", "malware prevention"]
            ),
            KnowledgeBaseEntry(
                id="kb-004",
                category=QuestionCategory.INCIDENT_RESPONSE,
                question="What are the phases of incident response?",
                answer="The incident response lifecycle includes: 1) Preparation, 2) Detection and Analysis, 3) Containment, Eradication, and Recovery, 4) Post-Incident Activity. Each phase is critical for effective incident handling and organizational learning.",
                keywords=["incident response", "lifecycle", "containment", "recovery"],
                related_topics=["incident handling", "forensics", "business continuity"]
            ),
            KnowledgeBaseEntry(
                id="kb-005",
                category=QuestionCategory.OSINT,
                question="What is OSINT?",
                answer="Open Source Intelligence (OSINT) is the collection and analysis of information from publicly available sources. In cybersecurity, OSINT helps identify threats, assess vulnerabilities, and investigate incidents using data from social media, websites, public databases, and other open sources.",
                keywords=["osint", "intelligence", "reconnaissance", "investigation"],
                related_topics=["threat intelligence", "digital forensics", "reconnaissance"]
            ),
            KnowledgeBaseEntry(
                id="kb-006",
                category=QuestionCategory.THREAT_ANALYSIS,
                question="What is a zero-day vulnerability?",
                answer="A zero-day vulnerability is a security flaw unknown to the software vendor or without an available patch. Attackers exploit these vulnerabilities before developers can fix them, making them particularly dangerous. Organizations should implement defense-in-depth strategies to mitigate zero-day risks.",
                keywords=["zero-day", "vulnerability", "exploit", "patch"],
                related_topics=["vulnerability management", "threat intelligence", "security updates"]
            ),
            KnowledgeBaseEntry(
                id="kb-007",
                category=QuestionCategory.BEST_PRACTICES,
                question="What is defense in depth?",
                answer="Defense in depth is a security strategy that uses multiple layers of security controls throughout an IT system. If one layer fails, others continue to provide protection. This includes network security, endpoint protection, access controls, monitoring, and user awareness training.",
                keywords=["defense in depth", "layered security", "security controls"],
                related_topics=["security architecture", "risk management", "security controls"]
            ),
            KnowledgeBaseEntry(
                id="kb-008",
                category=QuestionCategory.TOOLS,
                question="What is a SIEM?",
                answer="Security Information and Event Management (SIEM) is a solution that provides real-time analysis of security alerts generated by applications and network hardware. SIEM systems collect, aggregate, and analyze log data to detect threats, ensure compliance, and support incident response.",
                keywords=["siem", "security monitoring", "log analysis", "threat detection"],
                related_topics=["security operations", "threat detection", "compliance"]
            )
        ]
    
    async def send_message(self, request: ChatRequest) -> ChatResponse:
        """
        Send a message to the chat assistant and get a response
        
        Args:
            request: Chat request with message and optional session ID
            
        Returns:
            Chat response with assistant's message
        """
        logger.info(f"Processing chat message: {request.message[:50]}...")
        
        # Get or create session
        if request.session_id:
            session = await self.get_session(request.session_id)
            if not session:
                session = await self._create_session(request.session_id)
        else:
            session_id = f"chat-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
            session = await self._create_session(session_id)
        
        # Add user message to session
        user_message = ChatMessage(
            role=MessageRole.USER,
            content=request.message,
            timestamp=datetime.utcnow(),
            metadata=None
        )
        session.messages.append(user_message)
        
        # Determine question category
        category = self._categorize_question(request.message)
        
        # Get relevant knowledge base entries
        kb_context = ""
        if request.use_knowledge_base:
            kb_entries = self._search_knowledge_base(request.message)
            if kb_entries:
                kb_context = "\n\n".join([
                    f"Knowledge: {entry.answer}" for entry in kb_entries[:2]
                ])
        
        # Generate AI response
        assistant_content = await self._generate_response(
            message=request.message,
            conversation_history=session.messages[-5:],  # Last 5 messages
            kb_context=kb_context,
            category=category
        )
        
        # Create assistant message
        assistant_message = ChatMessage(
            role=MessageRole.ASSISTANT,
            content=assistant_content,
            timestamp=datetime.utcnow(),
            metadata={"category": category.value}
        )
        session.messages.append(assistant_message)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(category, request.message)
        
        # Update session
        session.updated_at = datetime.utcnow()
        if request.context:
            session.context.update(request.context)
        
        await self._save_session(session)
        
        # Create response
        response = ChatResponse(
            session_id=session.session_id,
            message=assistant_message,
            suggestions=suggestions,
            sources=["Cybersecurity Knowledge Base", "IBM Granite AI"] if kb_context else ["IBM Granite AI"],
            confidence=0.85 if kb_context else 0.75
        )
        
        logger.info(f"Generated response for session {session.session_id}")
        return response
    
    async def _generate_response(
        self,
        message: str,
        conversation_history: List[ChatMessage],
        kb_context: str,
        category: QuestionCategory
    ) -> str:
        """Generate AI response using IBM Granite"""
        
        # Build conversation context
        history_text = "\n".join([
            f"{msg.role.value}: {msg.content}"
            for msg in conversation_history[:-1]  # Exclude current message
        ])
        
        # Create prompt
        kb_section = f"Relevant Knowledge:\n{kb_context}\n" if kb_context else ""
        history_section = f"Previous Conversation:\n{history_text}\n" if history_text else ""
        
        prompt = f"""You are a cybersecurity expert assistant helping users understand security concepts and threats.

{kb_section}{history_section}User Question: {message}

Provide a clear, accurate, and helpful response. Be concise but thorough. If discussing threats, include:
- Clear explanation
- Real-world examples
- Prevention/mitigation strategies
- Related concepts

Response:"""
        
        try:
            # Use AI service
            if self.ai_service.model:
                response = self.ai_service.model.generate_text(prompt=prompt)
                return response.strip()
            else:
                # Mock response for development
                return self._generate_mock_response(message, category, kb_context)
        except Exception as e:
            logger.error(f"AI response generation failed: {e}")
            return self._generate_mock_response(message, category, kb_context)
    
    def _generate_mock_response(self, message: str, category: QuestionCategory, kb_context: str) -> str:
        """Generate mock response for development"""
        
        if kb_context:
            # Extract first sentence from knowledge base
            kb_answer = kb_context.split('\n')[0].replace("Knowledge: ", "")
            return f"{kb_answer}\n\nWould you like me to explain this in more detail or discuss related security concepts?"
        
        # Category-based responses
        responses = {
            QuestionCategory.PHISHING: "Phishing is a social engineering attack where attackers impersonate legitimate entities to steal sensitive information. Common indicators include urgent language, suspicious links, and requests for credentials. Always verify sender authenticity and hover over links before clicking.",
            QuestionCategory.MALWARE_ANALYSIS: "Malware analysis involves examining malicious software to understand its behavior, capabilities, and impact. This includes static analysis (examining code without execution) and dynamic analysis (observing behavior in a controlled environment).",
            QuestionCategory.MITRE_ATTACK: "The MITRE ATT&CK framework is a comprehensive knowledge base of adversary tactics and techniques. It helps security teams understand attack patterns, improve detection capabilities, and assess security posture.",
            QuestionCategory.INCIDENT_RESPONSE: "Effective incident response follows a structured approach: Preparation, Detection & Analysis, Containment, Eradication & Recovery, and Post-Incident Activity. Each phase is critical for minimizing impact and improving future response.",
            QuestionCategory.OSINT: "OSINT (Open Source Intelligence) involves gathering information from publicly available sources. In cybersecurity, it's used for threat intelligence, vulnerability assessment, and incident investigation.",
            QuestionCategory.THREAT_ANALYSIS: "Threat analysis involves identifying, assessing, and prioritizing potential security threats. This includes understanding threat actors, their capabilities, motivations, and likely attack vectors.",
            QuestionCategory.BEST_PRACTICES: "Security best practices include implementing defense in depth, regular security updates, strong authentication, least privilege access, security awareness training, and continuous monitoring.",
            QuestionCategory.TOOLS: "Security tools help automate detection, analysis, and response. Common categories include SIEM, EDR, vulnerability scanners, threat intelligence platforms, and forensic tools.",
            QuestionCategory.GENERAL: "I'm here to help with cybersecurity questions. I can explain security concepts, analyze threats, discuss incident response, and provide guidance on security best practices."
        }
        
        return responses.get(category, responses[QuestionCategory.GENERAL])
    
    def _categorize_question(self, message: str) -> QuestionCategory:
        """Categorize the user's question"""
        message_lower = message.lower()
        
        # Keyword-based categorization
        if any(word in message_lower for word in ["phishing", "phish", "email attack", "spear phishing"]):
            return QuestionCategory.PHISHING
        elif any(word in message_lower for word in ["malware", "virus", "ransomware", "trojan", "worm"]):
            return QuestionCategory.MALWARE_ANALYSIS
        elif any(word in message_lower for word in ["mitre", "att&ck", "attack", "tactic", "technique"]):
            return QuestionCategory.MITRE_ATTACK
        elif any(word in message_lower for word in ["incident", "response", "containment", "eradication"]):
            return QuestionCategory.INCIDENT_RESPONSE
        elif any(word in message_lower for word in ["osint", "open source", "reconnaissance", "footprint"]):
            return QuestionCategory.OSINT
        elif any(word in message_lower for word in ["threat", "vulnerability", "exploit", "zero-day"]):
            return QuestionCategory.THREAT_ANALYSIS
        elif any(word in message_lower for word in ["best practice", "security control", "defense", "protection"]):
            return QuestionCategory.BEST_PRACTICES
        elif any(word in message_lower for word in ["tool", "siem", "edr", "scanner", "software"]):
            return QuestionCategory.TOOLS
        else:
            return QuestionCategory.GENERAL
    
    def _search_knowledge_base(self, query: str) -> List[KnowledgeBaseEntry]:
        """Search knowledge base for relevant entries"""
        query_lower = query.lower()
        results = []
        
        for entry in self.knowledge_base:
            # Check if query matches keywords or question
            if any(keyword in query_lower for keyword in entry.keywords):
                results.append(entry)
            elif any(word in entry.question.lower() for word in query_lower.split()):
                results.append(entry)
        
        return results[:3]  # Return top 3 matches
    
    def _generate_suggestions(self, category: QuestionCategory, message: str) -> List[str]:
        """Generate follow-up question suggestions"""
        suggestions_map = {
            QuestionCategory.PHISHING: [
                "How can I detect phishing emails?",
                "What are common phishing techniques?",
                "How to report phishing attempts?"
            ],
            QuestionCategory.MALWARE_ANALYSIS: [
                "What tools are used for malware analysis?",
                "How to prevent malware infections?",
                "What is the difference between static and dynamic analysis?"
            ],
            QuestionCategory.MITRE_ATTACK: [
                "What are the main MITRE ATT&CK tactics?",
                "How to use MITRE ATT&CK for threat detection?",
                "What are common attack techniques?"
            ],
            QuestionCategory.INCIDENT_RESPONSE: [
                "What is the incident response lifecycle?",
                "How to contain a security incident?",
                "What tools are needed for incident response?"
            ],
            QuestionCategory.OSINT: [
                "What are common OSINT tools?",
                "How to conduct OSINT investigations?",
                "What are OSINT best practices?"
            ],
            QuestionCategory.THREAT_ANALYSIS: [
                "What is threat intelligence?",
                "How to assess threat severity?",
                "What are indicators of compromise?"
            ],
            QuestionCategory.BEST_PRACTICES: [
                "What is defense in depth?",
                "How to implement security controls?",
                "What are essential security practices?"
            ],
            QuestionCategory.TOOLS: [
                "What is a SIEM system?",
                "What are EDR solutions?",
                "How to choose security tools?"
            ],
            QuestionCategory.GENERAL: [
                "Tell me about common cyber threats",
                "How to improve security posture?",
                "What is threat intelligence?"
            ]
        }
        
        return suggestions_map.get(category, suggestions_map[QuestionCategory.GENERAL])
    
    async def _create_session(self, session_id: str) -> ChatSession:
        """Create a new chat session"""
        session = ChatSession(
            session_id=session_id,
            user_id=None,
            messages=[],
            context={},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True
        )
        return session
    
    async def _save_session(self, session: ChatSession) -> None:
        """Save chat session to database"""
        try:
            db: Any = get_database()
            collection = db[self.sessions_collection]
            
            session_dict = session.model_dump()
            await collection.update_one(
                {"session_id": session.session_id},
                {"$set": session_dict},
                upsert=True
            )
            
            logger.info(f"Saved session {session.session_id}")
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
    
    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get chat session by ID"""
        try:
            db: Any = get_database()
            collection = db[self.sessions_collection]
            
            session_dict = await collection.find_one({"session_id": session_id})
            if session_dict:
                session_dict.pop("_id", None)
                return ChatSession(**session_dict)
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve session {session_id}: {e}")
            return None
    
    async def list_sessions(self, user_id: Optional[str] = None, limit: int = 10) -> ChatSessionListResponse:
        """List chat sessions"""
        try:
            db: Any = get_database()
            collection = db[self.sessions_collection]
            
            query: Dict[str, Any] = {"is_active": True}
            if user_id:
                query["user_id"] = user_id
            
            total = await collection.count_documents(query)
            cursor = collection.find(query).sort("updated_at", -1).limit(limit)
            
            sessions = []
            async for session_dict in cursor:
                session_dict.pop("_id", None)
                sessions.append(ChatSession(**session_dict))
            
            return ChatSessionListResponse(sessions=sessions, total=total)
        except Exception as e:
            logger.error(f"Failed to list sessions: {e}")
            return ChatSessionListResponse(sessions=[], total=0)
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a chat session"""
        try:
            db: Any = get_database()
            collection = db[self.sessions_collection]
            
            result = await collection.update_one(
                {"session_id": session_id},
                {"$set": {"is_active": False}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            return False
    
    async def get_analytics(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> ChatAnalyticsResponse:
        """Get chat analytics"""
        try:
            db: Any = get_database()
            collection = db[self.sessions_collection]
            
            query: Dict[str, Any] = {"is_active": True}
            if start_date or end_date:
                date_query: Dict[str, Any] = {}
                if start_date:
                    date_query["$gte"] = start_date
                if end_date:
                    date_query["$lte"] = end_date
                query["created_at"] = date_query
            
            sessions = []
            async for session_dict in collection.find(query):
                session_dict.pop("_id", None)
                sessions.append(ChatSession(**session_dict))
            
            total_sessions = len(sessions)
            total_messages = sum(len(s.messages) for s in sessions)
            avg_messages = total_messages / total_sessions if total_sessions > 0 else 0
            
            # Count categories
            categories: Dict[str, int] = {}
            questions: List[str] = []
            
            for session in sessions:
                for msg in session.messages:
                    if msg.role == MessageRole.ASSISTANT and msg.metadata:
                        cat = msg.metadata.get("category", "general")
                        categories[cat] = categories.get(cat, 0) + 1
                    elif msg.role == MessageRole.USER:
                        questions.append(msg.content)
            
            # Get most common questions (simplified)
            common_questions = list(set(questions))[:5]
            
            return ChatAnalyticsResponse(
                total_sessions=total_sessions,
                total_messages=total_messages,
                avg_messages_per_session=round(avg_messages, 2),
                top_categories=categories,
                common_questions=common_questions
            )
        except Exception as e:
            logger.error(f"Failed to get analytics: {e}")
            return ChatAnalyticsResponse(
                total_sessions=0,
                total_messages=0,
                avg_messages_per_session=0.0,
                top_categories={},
                common_questions=[]
            )

# Made with Bob
