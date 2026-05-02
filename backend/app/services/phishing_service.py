"""
Phishing Detection Service
Handles phishing analysis using AI and external APIs
"""
from app.services.ai_service import AIService
from app.integrations.virustotal import VirusTotalClient
from app.database.mongodb import get_database
from datetime import datetime
import uuid
import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class PhishingService:
    """Service for phishing detection and analysis"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.vt_client = VirusTotalClient()
    
    async def analyze(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze content for phishing indicators
        
        Args:
            request_data: Dictionary with content_type, content, sender, metadata
            
        Returns:
            Dictionary with analysis results
        """
        analysis_id = str(uuid.uuid4())
        logger.info(f"Starting phishing analysis: {analysis_id}")
        
        try:
            # Extract URLs from content
            urls = self._extract_urls(request_data['content'])
            logger.info(f"Found {len(urls)} URLs in content")
            
            # Check URLs with VirusTotal
            vt_results = None
            if urls:
                vt_results = await self.vt_client.check_urls(urls)
                logger.info(f"VirusTotal scan completed for {len(vt_results)} URLs")
            
            # Perform AI analysis
            ai_analysis = await self.ai_service.analyze_phishing({
                'content': request_data['content'],
                'content_type': request_data['content_type'],
                'urls': urls,
                'vt_results': vt_results,
                'sender': request_data.get('sender')
            })
            
            # Store analysis in database
            analysis_doc = {
                'analysis_id': analysis_id,
                'content_type': request_data['content_type'],
                'content': request_data['content'],
                'sender': request_data.get('sender'),
                'metadata': request_data.get('metadata', {}),
                'urls_found': urls,
                'virustotal_results': vt_results,
                'ai_analysis': ai_analysis,
                'status': 'completed',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            db = get_database()
            await db.phishing_analyses.insert_one(analysis_doc)
            logger.info(f"Analysis {analysis_id} stored in database")
            
            # Return response
            return {
                'analysis_id': analysis_id,
                'threat_score': ai_analysis['threat_score'],
                'is_phishing': ai_analysis['is_phishing'],
                'confidence': ai_analysis['confidence'],
                'indicators': ai_analysis['indicators'],
                'explanation': ai_analysis['explanation'],
                'recommendations': ai_analysis['recommendations'],
                'virustotal_results': vt_results,
                'created_at': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Phishing analysis failed: {e}", exc_info=True)
            # Store failed analysis
            db = get_database()
            await db.phishing_analyses.insert_one({
                'analysis_id': analysis_id,
                'content_type': request_data['content_type'],
                'content': request_data['content'],
                'status': 'failed',
                'error': str(e),
                'created_at': datetime.utcnow()
            })
            raise
    
    def _extract_urls(self, content: str) -> List[str]:
        """
        Extract URLs from content
        
        Args:
            content: Text content to extract URLs from
            
        Returns:
            List of URLs found
        """
        # URL regex pattern
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, content)
        
        # Remove duplicates and limit to first 10
        unique_urls = list(dict.fromkeys(urls))[:10]
        
        return unique_urls
    
    async def get_analysis(self, analysis_id: str) -> Dict[str, Any]:
        """
        Get analysis by ID
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Analysis document
        """
        db = get_database()
        analysis = await db.phishing_analyses.find_one({'analysis_id': analysis_id})
        
        if not analysis:
            raise ValueError(f"Analysis {analysis_id} not found")
        
        # Remove MongoDB _id field
        analysis.pop('_id', None)
        
        return analysis
    
    async def get_history(self, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        """
        Get analysis history
        
        Args:
            limit: Number of results to return
            skip: Number of results to skip
            
        Returns:
            Dictionary with total count and analyses
        """
        db = get_database()
        
        # Get total count
        total = await db.phishing_analyses.count_documents({})
        
        # Get analyses
        cursor = db.phishing_analyses.find(
            {},
            {'_id': 0}  # Exclude MongoDB _id
        ).sort('created_at', -1).skip(skip).limit(limit)
        
        analyses = await cursor.to_list(length=limit)
        
        return {
            'total': total,
            'analyses': analyses
        }
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get phishing analysis statistics
        
        Returns:
            Dictionary with statistics
        """
        db = get_database()
        
        # Total analyses
        total = await db.phishing_analyses.count_documents({})
        
        # Phishing detected
        phishing_count = await db.phishing_analyses.count_documents({
            'ai_analysis.is_phishing': True
        })
        
        # Average threat score
        pipeline = [
            {
                '$group': {
                    '_id': None,
                    'avg_threat_score': {'$avg': '$ai_analysis.threat_score'}
                }
            }
        ]
        
        result = await db.phishing_analyses.aggregate(pipeline).to_list(1)
        avg_threat_score = result[0]['avg_threat_score'] if result else 0
        
        # By content type
        pipeline = [
            {
                '$group': {
                    '_id': '$content_type',
                    'count': {'$sum': 1}
                }
            }
        ]
        
        by_type = await db.phishing_analyses.aggregate(pipeline).to_list(10)
        
        return {
            'total_analyses': total,
            'phishing_detected': phishing_count,
            'legitimate': total - phishing_count,
            'average_threat_score': round(avg_threat_score, 2),
            'by_content_type': {item['_id']: item['count'] for item in by_type}
        }

# Made with Bob
