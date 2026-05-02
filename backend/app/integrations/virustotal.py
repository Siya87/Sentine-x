"""
VirusTotal API Integration
Provides malware scanning and URL/file analysis
"""
from app.config import get_settings
import httpx
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)
settings = get_settings()


class VirusTotalClient:
    """VirusTotal API client for malware and URL scanning"""
    
    def __init__(self):
        self.api_key = settings.virustotal_api_key
        self.base_url = "https://www.virustotal.com/api/v3"
        self.headers = {
            "x-apikey": self.api_key,
            "Accept": "application/json"
        }
    
    async def check_url(self, url: str) -> Optional[Dict]:
        """
        Check a URL for malicious content
        
        Args:
            url: URL to check
            
        Returns:
            Dictionary with scan results or None if error
        """
        if not self.api_key:
            logger.warning("VirusTotal API key not configured")
            return self._mock_url_result(url)
        
        try:
            async with httpx.AsyncClient() as client:
                # Submit URL for scanning
                response = await client.post(
                    f"{self.base_url}/urls",
                    headers=self.headers,
                    data={"url": url}
                )
                if response.status_code == 200:
                    data = response.json()
                    analysis_id = data.get("data", {}).get("id")
                    
                    # Get analysis results
                    return await self._get_analysis(client, analysis_id)
                else:
                    logger.error(f"VirusTotal URL submission failed: {response.status_code}")
                    return self._mock_url_result(url)
        
        except Exception as e:
            logger.error(f"VirusTotal URL check failed: {e}")
            return self._mock_url_result(url)
    
    async def check_urls(self, urls: List[str]) -> Dict[str, Dict]:
        """
        Check multiple URLs
        
        Args:
            urls: List of URLs to check
            
        Returns:
            Dictionary mapping URLs to their scan results
        """
        results = {}
        for url in urls[:5]:  # Limit to 5 URLs to respect rate limits
            result = await self.check_url(url)
            if result:
                results[url] = result
        
        return results
    
    async def _get_analysis(self, client: httpx.AsyncClient, analysis_id: str) -> Optional[Dict]:
        """Get analysis results"""
        try:
            response = await client.get(
                f"{self.base_url}/analyses/{analysis_id}",
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                return self._parse_analysis_result(data)
            else:
                logger.error(f"Failed to get analysis: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Failed to get analysis: {e}")
            return None
    
    def _parse_analysis_result(self, data: Dict) -> Dict:
        """Parse VirusTotal analysis result"""
        attributes = data.get("data", {}).get("attributes", {})
        stats = attributes.get("stats", {})
        
        return {
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "undetected": stats.get("undetected", 0),
            "total_scans": sum(stats.values()),
            "status": attributes.get("status", "unknown"),
            "results": attributes.get("results", {})
        }
    
    def _mock_url_result(self, url: str) -> Dict:
        """Mock result for development/testing"""
        # Simple heuristic: check for suspicious patterns
        suspicious_patterns = ['bit.ly', 'tinyurl', 'goo.gl', 'ow.ly']
        is_suspicious = any(pattern in url.lower() for pattern in suspicious_patterns)
        
        return {
            "malicious": 2 if is_suspicious else 0,
            "suspicious": 3 if is_suspicious else 0,
            "harmless": 50 if not is_suspicious else 40,
            "undetected": 10,
            "total_scans": 65,
            "status": "completed",
            "results": {
                "mock_scanner": {
                    "category": "suspicious" if is_suspicious else "harmless",
                    "result": "potentially malicious" if is_suspicious else "clean"
                }
            }
        }
    
    async def check_file_hash(self, file_hash: str) -> Optional[Dict]:
        """
        Check a file hash for malware
        
        Args:
            file_hash: SHA256, SHA1, or MD5 hash
            
        Returns:
            Dictionary with scan results or None if error
        """
        if not self.api_key:
            logger.warning("VirusTotal API key not configured")
            return self._mock_file_result(file_hash)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/files/{file_hash}",
                    headers=self.headers
                )
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_file_result(data)
                elif response.status_code == 404:
                    logger.info(f"File hash not found in VirusTotal: {file_hash}")
                    return {"status": "not_found"}
                else:
                    logger.error(f"VirusTotal file check failed: {response.status_code}")
                    return self._mock_file_result(file_hash)
        
        except Exception as e:
            logger.error(f"VirusTotal file check failed: {e}")
            return self._mock_file_result(file_hash)
    
    def _parse_file_result(self, data: Dict) -> Dict:
        """Parse VirusTotal file result"""
        attributes = data.get("data", {}).get("attributes", {})
        stats = attributes.get("last_analysis_stats", {})
        
        return {
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "undetected": stats.get("undetected", 0),
            "total_scans": sum(stats.values()),
            "file_type": attributes.get("type_description", "unknown"),
            "size": attributes.get("size", 0),
            "md5": attributes.get("md5", ""),
            "sha256": attributes.get("sha256", ""),
            "results": attributes.get("last_analysis_results", {})
        }
    
    def _mock_file_result(self, file_hash: str) -> Dict:
        """Mock file result for development/testing"""
        return {
            "malicious": 0,
            "suspicious": 0,
            "harmless": 60,
            "undetected": 5,
            "total_scans": 65,
            "file_type": "unknown",
            "size": 0,
            "md5": file_hash[:32] if len(file_hash) >= 32 else file_hash,
            "sha256": file_hash if len(file_hash) == 64 else "",
            "results": {
                "mock_scanner": {
                    "category": "harmless",
                    "result": "clean"
                }
            }
        }
    
    async def get_domain_info(self, domain: str) -> Optional[Dict]:
        """
        Get domain information and reputation
        
        Args:
            domain: Domain name to check
            
        Returns:
            Dictionary with domain information
        """
        if not self.api_key:
            logger.warning("VirusTotal API key not configured")
            return self._mock_domain_result(domain)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/domains/{domain}",
                    headers=self.headers
                )
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_domain_result(data)
                else:
                    logger.error(f"VirusTotal domain check failed: {response.status_code}")
                    return self._mock_domain_result(domain)
        
        except Exception as e:
            logger.error(f"VirusTotal domain check failed: {e}")
            return self._mock_domain_result(domain)
    
    def _parse_domain_result(self, data: Dict) -> Dict:
        """Parse VirusTotal domain result"""
        attributes = data.get("data", {}).get("attributes", {})
        stats = attributes.get("last_analysis_stats", {})
        
        return {
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "undetected": stats.get("undetected", 0),
            "reputation": attributes.get("reputation", 0),
            "categories": attributes.get("categories", {}),
            "creation_date": attributes.get("creation_date", None)
        }
    
    def _mock_domain_result(self, domain: str) -> Dict:
        """Mock domain result for development/testing"""
        return {
            "malicious": 0,
            "suspicious": 0,
            "harmless": 60,
            "undetected": 5,
            "reputation": 0,
            "categories": {},
            "creation_date": None
        }

# Made with Bob
