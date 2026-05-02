"""
IBM Granite AI Service Integration
Handles all AI-powered analysis using IBM Granite models
"""
from app.config import get_settings
import logging
import json
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)
settings = get_settings()


class AIService:
    """IBM Granite AI Service for cybersecurity analysis"""
    
    def __init__(self):
        """Initialize IBM Granite model"""
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize IBM Granite model connection"""
        try:
            from ibm_watson_machine_learning.foundation_models import Model  # type: ignore
            
            self.model = Model(
                model_id="ibm/granite-13b-instruct-v2",
                credentials={
                    "url": settings.ibm_watsonx_url,
                    "apikey": settings.ibm_cloud_api_key
                },
                project_id=settings.ibm_project_id,
                params={
                    "decoding_method": "greedy",
                    "max_new_tokens": 1500,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                }
            )
            logger.info("IBM Granite model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize IBM Granite model: {e}")
            # For development, we'll create a mock model
            self.model = None
    
    async def generate_incident_report_content(self, prompt: str) -> Dict[str, Any]:
        """
        Generate incident report content using IBM Granite
        
        Args:
            prompt: Prompt for report generation
            
        Returns:
            Dictionary with executive_summary and impact_description
        """
        try:
            if self.model:
                response = self.model.generate_text(prompt=prompt)
                result = self._parse_report_response(response)
            else:
                # Mock response for development
                result = self._mock_report_content()
            
            logger.info("Incident report content generated")
            return result
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return self._mock_report_content()
    
    def _parse_report_response(self, response: str) -> Dict[str, Any]:
        """Parse IBM Granite response for report generation"""
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse report response: {e}")
        
        return self._mock_report_content()
    
    def _mock_report_content(self) -> Dict[str, Any]:
        """Mock report content for development"""
        return {
            "executive_summary": "A security incident was detected and is currently under investigation. The incident response team has been activated and is working to contain the threat and assess the full scope of the impact.",
            "impact_description": "The incident has resulted in potential impact on operations. Affected systems have been identified and are being monitored closely."
        }
    
    async def analyze_phishing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze content for phishing indicators using IBM Granite
        
        Args:
            data: Dictionary containing content, content_type, urls, and vt_results
            
        Returns:
            Dictionary with threat_score, is_phishing, confidence, indicators, explanation, recommendations
        """
        prompt = self._create_phishing_prompt(data)
        
        try:
            if self.model:
                response = self.model.generate_text(prompt=prompt)
                result = self._parse_phishing_response(response)
            else:
                # Mock response for development
                result = self._mock_phishing_analysis(data)
            
            logger.info(f"Phishing analysis completed with threat score: {result['threat_score']}")
            return result
            
        except Exception as e:
            logger.error(f"Phishing analysis failed: {e}")
            return self._mock_phishing_analysis(data)
    
    def _create_phishing_prompt(self, data: Dict[str, Any]) -> str:
        """Create prompt for phishing analysis"""
        return f"""You are a cybersecurity expert specializing in phishing detection.

Analyze the following content for phishing indicators:

Content Type: {data.get('content_type', 'unknown')}
Content: {data.get('content', '')[:1000]}
URLs Found: {', '.join(data.get('urls', [])[:5])}
VirusTotal Results: {json.dumps(data.get('vt_results', {}), indent=2) if data.get('vt_results') else 'Not available'}

Provide a detailed analysis in JSON format:
{{
  "threat_score": <0-100>,
  "is_phishing": <true/false>,
  "confidence": <0-100>,
  "indicators": [
    {{
      "type": "urgency|spoofing|suspicious_link|grammar|impersonation|etc",
      "description": "detailed explanation",
      "severity": "low|medium|high|critical"
    }}
  ],
  "explanation": "comprehensive analysis of why this is or isn't phishing",
  "recommendations": [
    "specific action items for the user"
  ]
}}

Be thorough and precise in your analysis. Consider:
- Urgency and pressure tactics
- Sender authenticity
- URL legitimacy
- Grammar and spelling
- Request for sensitive information
- Impersonation attempts"""
    
    def _parse_phishing_response(self, response: str) -> Dict[str, Any]:
        """Parse IBM Granite response for phishing analysis"""
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse phishing response: {e}")
        
        # Return default structure if parsing fails
        return {
            "threat_score": 50,
            "is_phishing": False,
            "confidence": 50,
            "indicators": [],
            "explanation": "Analysis completed but response parsing failed",
            "recommendations": ["Manual review recommended"]
        }
    
    def _mock_phishing_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock phishing analysis for development"""
        content = data.get('content', '').lower()
        urls = data.get('urls', [])
        
        # Simple heuristic-based mock analysis
        threat_score = 0
        indicators = []
        
        # Check for urgency keywords
        urgency_keywords = ['urgent', 'immediately', 'suspend', 'verify', 'confirm', 'expire']
        if any(keyword in content for keyword in urgency_keywords):
            threat_score += 30
            indicators.append({
                "type": "urgency",
                "description": "Content contains urgency language",
                "severity": "high"
            })
        
        # Check for suspicious URLs
        if urls:
            threat_score += 20
            indicators.append({
                "type": "suspicious_link",
                "description": f"Contains {len(urls)} URL(s) that require verification",
                "severity": "medium"
            })
        
        # Check for credential requests
        if any(word in content for word in ['password', 'account', 'login', 'credential']):
            threat_score += 25
            indicators.append({
                "type": "credential_request",
                "description": "Requests sensitive credential information",
                "severity": "critical"
            })
        
        is_phishing = threat_score >= 50
        
        return {
            "threat_score": min(threat_score, 100),
            "is_phishing": is_phishing,
            "confidence": 75,
            "indicators": indicators,
            "explanation": f"Analysis detected {len(indicators)} phishing indicators. " + 
                          ("This appears to be a phishing attempt." if is_phishing else "This appears to be legitimate."),
            "recommendations": [
                "Do not click on any links" if is_phishing else "Exercise caution",
                "Verify sender authenticity",
                "Report to security team if suspicious"
            ]
        }
    
    async def generate_osint_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate OSINT investigation summary using IBM Granite
        
        Args:
            data: Dictionary containing target, breach_data, ip_reputation, etc.
            
        Returns:
            Dictionary with risk_score, summary, key_findings, threats, recommendations
        """
        prompt = self._create_osint_prompt(data)
        
        try:
            if self.model:
                response = self.model.generate_text(prompt=prompt)
                result = self._parse_osint_response(response)
            else:
                result = self._mock_osint_summary(data)
            
            logger.info(f"OSINT summary generated for target: {data.get('target')}")
            return result
            
        except Exception as e:
            logger.error(f"OSINT summary generation failed: {e}")
            return self._mock_osint_summary(data)
    
    def _create_osint_prompt(self, data: Dict[str, Any]) -> str:
        """Create prompt for OSINT summary"""
        return f"""You are an OSINT analyst creating an investigation summary.

Target Information:
- Target: {data.get('target')}
- Type: {data.get('target_type')}

Data Collected:
- Breach Data: {json.dumps(data.get('breach_data', []), indent=2)}
- IP Reputation: {json.dumps(data.get('ip_reputation', {}), indent=2)}
- Social Profiles: {json.dumps(data.get('social_profiles', []), indent=2)}

Create a comprehensive investigation summary in JSON format:
{{
  "risk_score": <0-100>,
  "risk_level": "low|medium|high|critical",
  "summary": "executive summary of findings",
  "key_findings": [
    "finding 1",
    "finding 2"
  ],
  "threats_identified": [
    {{
      "threat": "description",
      "severity": "low|medium|high|critical",
      "evidence": "supporting evidence"
    }}
  ],
  "recommendations": [
    "actionable recommendations"
  ]
}}

Be objective and evidence-based in your analysis."""
    
    def _parse_osint_response(self, response: str) -> Dict[str, Any]:
        """Parse IBM Granite response for OSINT summary"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse OSINT response: {e}")
        
        return {
            "risk_score": 50,
            "risk_level": "medium",
            "summary": "Investigation completed",
            "key_findings": [],
            "threats_identified": [],
            "recommendations": []
        }
    
    def _mock_osint_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock OSINT summary for development"""
        breach_data = data.get('breach_data', [])
        # breach_data is already a list, not a dict
        breaches = breach_data if isinstance(breach_data, list) else []
        
        risk_score = len(breaches) * 15
        risk_level = "low" if risk_score < 30 else "medium" if risk_score < 60 else "high"
        
        return {
            "risk_score": min(risk_score, 100),
            "risk_level": risk_level,
            "summary": f"Investigation of {data.get('target')} found {len(breaches)} data breach(es)",
            "key_findings": [
                f"Target found in {len(breaches)} data breach(es)",
                "No malicious activity detected" if risk_score < 50 else "Elevated risk detected"
            ],
            "threats_identified": [
                {
                    "threat": "Data exposure in breaches",
                    "severity": risk_level,
                    "evidence": f"Found in {len(breaches)} breach(es)"
                }
            ] if breaches else [],
            "recommendations": [
                "Change passwords for affected accounts",
                "Enable two-factor authentication",
                "Monitor for suspicious activity"
            ]
        }
    
    async def generate_incident_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate incident report using IBM Granite
        
        Args:
            data: Dictionary containing incident details
            
        Returns:
            Dictionary with report sections
        """
        # Implementation will be added when building the report generator feature
        logger.info("Generating incident report...")
        return {
            "title": f"Incident Report: {data.get('incident_type', 'Unknown')}",
            "executive_summary": "Report generation in progress",
            "sections": {}
        }
    
    async def chat(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Chat with IBM Granite AI assistant
        
        Args:
            message: User message
            history: Conversation history
            
        Returns:
            AI response
        """
        # Implementation will be added when building the chat assistant feature
        logger.info(f"Processing chat message: {message[:50]}...")
        return "Chat functionality will be implemented in the chat assistant feature."

# Made with Bob
