"""
Shodan API Integration
Provides threat intelligence and host information from Shodan
"""
import httpx
from app.config import get_settings
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)
settings = get_settings()


class ShodanClient:
    """Shodan API client for threat intelligence"""
    
    def __init__(self):
        """Initialize Shodan client"""
        self.api_key = settings.shodan_api_key
        self.base_url = "https://api.shodan.io"
        self.timeout = 30.0
    
    async def search_hosts(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search for hosts using Shodan query
        
        Args:
            query: Shodan search query
            limit: Maximum number of results
            
        Returns:
            List of host information dictionaries
        """
        if not self.api_key or self.api_key == "your_shodan_api_key_here":
            logger.warning("Shodan API key not configured, using mock data")
            return self._mock_search_results(query, limit)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/shodan/host/search",
                    params={
                        "key": self.api_key,
                        "query": query,
                        "limit": min(limit, 100)
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("matches", [])
                else:
                    logger.error(f"Shodan search failed: {response.status_code}")
                    return self._mock_search_results(query, limit)
                    
        except Exception as e:
            logger.error(f"Shodan search error: {e}")
            return self._mock_search_results(query, limit)
    
    async def get_host_info(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific host
        
        Args:
            ip: IP address to lookup
            
        Returns:
            Host information dictionary or None
        """
        if not self.api_key or self.api_key == "your_shodan_api_key_here":
            logger.warning("Shodan API key not configured, using mock data")
            return self._mock_host_info(ip)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/shodan/host/{ip}",
                    params={"key": self.api_key}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Shodan host lookup failed: {response.status_code}")
                    return self._mock_host_info(ip)
                    
        except Exception as e:
            logger.error(f"Shodan host lookup error: {e}")
            return self._mock_host_info(ip)
    
    async def get_vulnerabilities(self, query: str = "vuln:*") -> List[Dict[str, Any]]:
        """
        Search for hosts with known vulnerabilities
        
        Args:
            query: Vulnerability search query
            
        Returns:
            List of vulnerable hosts
        """
        return await self.search_hosts(query, limit=50)
    
    async def get_malware_c2(self) -> List[Dict[str, Any]]:
        """
        Get malware command and control servers
        
        Returns:
            List of C2 servers
        """
        query = "category:malware"
        return await self.search_hosts(query, limit=50)
    
    async def get_ransomware_infrastructure(self) -> List[Dict[str, Any]]:
        """
        Get ransomware infrastructure
        
        Returns:
            List of ransomware-related hosts
        """
        query = "ransomware"
        return await self.search_hosts(query, limit=50)
    
    async def get_exposed_services(self, service: str) -> List[Dict[str, Any]]:
        """
        Get hosts with exposed services
        
        Args:
            service: Service name (e.g., 'rdp', 'ssh', 'mongodb')
            
        Returns:
            List of hosts with exposed service
        """
        query = f"product:{service}"
        return await self.search_hosts(query, limit=100)
    
    async def get_country_threats(self, country_code: str) -> List[Dict[str, Any]]:
        """
        Get threats from a specific country
        
        Args:
            country_code: Two-letter country code
            
        Returns:
            List of threats from country
        """
        query = f"country:{country_code}"
        return await self.search_hosts(query, limit=100)
    
    def _mock_search_results(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Generate mock search results for development"""
        mock_results = []
        
        for i in range(min(limit, 10)):
            mock_results.append({
                "ip_str": f"192.168.{i}.{100 + i}",
                "port": 443 if i % 2 == 0 else 80,
                "hostnames": [f"host{i}.example.com"],
                "domains": ["example.com"],
                "org": f"Organization {i}",
                "isp": f"ISP {i}",
                "asn": f"AS{12345 + i}",
                "country_code": ["US", "CN", "RU", "DE", "GB"][i % 5],
                "country_name": ["United States", "China", "Russia", "Germany", "United Kingdom"][i % 5],
                "city": ["New York", "Beijing", "Moscow", "Berlin", "London"][i % 5],
                "latitude": [40.7128, 39.9042, 55.7558, 52.5200, 51.5074][i % 5],
                "longitude": [-74.0060, 116.4074, 37.6173, 13.4050, -0.1278][i % 5],
                "os": "Linux" if i % 2 == 0 else "Windows",
                "vulns": ["CVE-2021-44228", "CVE-2021-45046"] if i % 3 == 0 else [],
                "tags": ["malware", "botnet"] if i % 4 == 0 else [],
                "timestamp": datetime.utcnow().isoformat(),
                "data": f"Mock service data for {query}"
            })
        
        return mock_results
    
    def _mock_host_info(self, ip: str) -> Dict[str, Any]:
        """Generate mock host information"""
        return {
            "ip_str": ip,
            "hostnames": [f"host.example.com"],
            "domains": ["example.com"],
            "ports": [80, 443, 22],
            "vulns": ["CVE-2021-44228"],
            "os": "Linux 4.15",
            "org": "Example Organization",
            "isp": "Example ISP",
            "asn": "AS12345",
            "country_code": "US",
            "country_name": "United States",
            "city": "New York",
            "region_code": "NY",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "last_update": datetime.utcnow().isoformat(),
            "tags": ["web-server"],
            "data": [
                {
                    "port": 443,
                    "transport": "tcp",
                    "product": "nginx",
                    "version": "1.18.0",
                    "ssl": {
                        "cert": {
                            "subject": {"CN": "example.com"},
                            "issuer": {"CN": "Let's Encrypt"},
                            "expired": False
                        }
                    }
                }
            ]
        }
    
    async def get_api_info(self) -> Dict[str, Any]:
        """
        Get Shodan API account information
        
        Returns:
            API account info
        """
        if not self.api_key or self.api_key == "your_shodan_api_key_here":
            return {
                "plan": "dev",
                "query_credits": 0,
                "scan_credits": 0,
                "usage": {"query": 0, "scan": 0},
                "unlocked": False
            }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api-info",
                    params={"key": self.api_key}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Shodan API info failed: {response.status_code}")
                    return {}
                    
        except Exception as e:
            logger.error(f"Shodan API info error: {e}")
            return {}


# Made with Bob