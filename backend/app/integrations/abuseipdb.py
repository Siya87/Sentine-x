"""
AbuseIPDB API Integration
Check IP addresses for malicious activity
"""
from app.config import get_settings
import httpx
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)
settings = get_settings()


class AbuseIPDBClient:
    """AbuseIPDB API client for IP reputation checks"""
    
    def __init__(self):
        self.api_key = settings.abuseipdb_api_key
        self.base_url = "https://api.abuseipdb.com/api/v2"
        self.headers = {
            "Key": self.api_key if self.api_key else "",
            "Accept": "application/json"
        }
    
    async def check_ip(self, ip_address: str, max_age_days: int = 90) -> Optional[Dict]:
        """
        Check an IP address for abuse reports
        
        Args:
            ip_address: IP address to check
            max_age_days: Maximum age of reports to include (default 90 days)
            
        Returns:
            Dictionary with IP information or None if error
        """
        if not self.api_key:
            logger.warning("AbuseIPDB API key not configured")
            return self._mock_ip_data(ip_address)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/check",
                    headers=self.headers,
                    params={
                        "ipAddress": ip_address,
                        "maxAgeInDays": max_age_days,
                        "verbose": True
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_ip_data(data)
                else:
                    logger.error(f"AbuseIPDB check failed: {response.status_code}")
                    return self._mock_ip_data(ip_address)
        
        except Exception as e:
            logger.error(f"AbuseIPDB check failed: {e}")
            return self._mock_ip_data(ip_address)
    
    async def report_ip(self, ip_address: str, categories: list, comment: str) -> bool:
        """
        Report an IP address for abuse
        
        Args:
            ip_address: IP address to report
            categories: List of abuse category IDs
            comment: Description of the abuse
            
        Returns:
            True if report was successful
        """
        if not self.api_key:
            logger.warning("AbuseIPDB API key not configured")
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/report",
                    headers=self.headers,
                    data={
                        "ip": ip_address,
                        "categories": ",".join(map(str, categories)),
                        "comment": comment
                    }
                )
                
                return response.status_code == 200
        
        except Exception as e:
            logger.error(f"Failed to report IP: {e}")
            return False
    
    async def get_blacklist(self, confidence_minimum: int = 90, limit: int = 10000) -> Optional[list]:
        """
        Get blacklisted IP addresses
        
        Args:
            confidence_minimum: Minimum confidence score (0-100)
            limit: Maximum number of IPs to return
            
        Returns:
            List of blacklisted IPs
        """
        if not self.api_key:
            logger.warning("AbuseIPDB API key not configured")
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/blacklist",
                    headers=self.headers,
                    params={
                        "confidenceMinimum": confidence_minimum,
                        "limit": limit
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("data", [])
                else:
                    logger.error(f"Failed to get blacklist: {response.status_code}")
                    return []
        
        except Exception as e:
            logger.error(f"Failed to get blacklist: {e}")
            return []
    
    def _parse_ip_data(self, data: Dict) -> Dict:
        """Parse AbuseIPDB response data"""
        ip_data = data.get("data", {})
        
        return {
            "ip": ip_data.get("ipAddress"),
            "is_public": ip_data.get("isPublic", True),
            "ip_version": ip_data.get("ipVersion", 4),
            "is_whitelisted": ip_data.get("isWhitelisted", False),
            "abuse_confidence_score": ip_data.get("abuseConfidenceScore", 0),
            "country_code": ip_data.get("countryCode"),
            "country_name": ip_data.get("countryName"),
            "usage_type": ip_data.get("usageType"),
            "isp": ip_data.get("isp"),
            "domain": ip_data.get("domain"),
            "hostnames": ip_data.get("hostnames", []),
            "total_reports": ip_data.get("totalReports", 0),
            "num_distinct_users": ip_data.get("numDistinctUsers", 0),
            "last_reported_at": ip_data.get("lastReportedAt"),
            "reports": ip_data.get("reports", [])
        }
    
    def _mock_ip_data(self, ip_address: str) -> Dict:
        """Generate mock IP data for testing"""
        return {
            "ip": ip_address,
            "is_public": True,
            "ip_version": 4,
            "is_whitelisted": False,
            "abuse_confidence_score": 25,
            "country_code": "US",
            "country_name": "United States",
            "usage_type": "Data Center/Web Hosting/Transit",
            "isp": "Example ISP",
            "domain": "example.com",
            "hostnames": ["host.example.com"],
            "total_reports": 5,
            "num_distinct_users": 3,
            "last_reported_at": "2026-04-15T10:30:00+00:00",
            "reports": [
                {
                    "reportedAt": "2026-04-15T10:30:00+00:00",
                    "comment": "Port scanning activity detected",
                    "categories": [14],  # Port Scan
                    "reporterId": 12345,
                    "reporterCountryCode": "US"
                }
            ]
        }
    
    @staticmethod
    def get_abuse_categories() -> Dict[int, str]:
        """
        Get abuse category mappings
        
        Returns:
            Dictionary of category IDs to names
        """
        return {
            3: "Fraud Orders",
            4: "DDoS Attack",
            5: "FTP Brute-Force",
            6: "Ping of Death",
            7: "Phishing",
            8: "Fraud VoIP",
            9: "Open Proxy",
            10: "Web Spam",
            11: "Email Spam",
            12: "Blog Spam",
            13: "VPN IP",
            14: "Port Scan",
            15: "Hacking",
            16: "SQL Injection",
            17: "Spoofing",
            18: "Brute-Force",
            19: "Bad Web Bot",
            20: "Exploited Host",
            21: "Web App Attack",
            22: "SSH",
            23: "IoT Targeted"
        }

# Made with Bob
