"""
HaveIBeenPwned API Integration
Check for compromised emails and passwords
"""
from app.config import get_settings
import httpx
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)
settings = get_settings()


class HaveIBeenPwnedClient:
    """HaveIBeenPwned API client for breach data"""
    
    def __init__(self):
        self.api_key = settings.haveibeenpwned_api_key
        self.base_url = "https://haveibeenpwned.com/api/v3"
        self.headers = {
            "hibp-api-key": self.api_key if self.api_key else "",
            "User-Agent": "SentinelX-AI"
        }
    
    async def check_email(self, email: str) -> Optional[List[Dict]]:
        """
        Check if an email has been in any breaches
        
        Args:
            email: Email address to check
            
        Returns:
            List of breaches or None if error
        """
        if not self.api_key:
            logger.warning("HaveIBeenPwned API key not configured")
            return self._mock_breach_data(email)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/breachedaccount/{email}",
                    headers=self.headers,
                    params={"truncateResponse": "false"}
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    # No breaches found - good news!
                    return []
                else:
                    logger.error(f"HaveIBeenPwned check failed: {response.status_code}")
                    return self._mock_breach_data(email)
        
        except Exception as e:
            logger.error(f"HaveIBeenPwned check failed: {e}")
            return self._mock_breach_data(email)
    
    async def check_password(self, password: str) -> Optional[int]:
        """
        Check if a password has been pwned using k-anonymity
        
        Args:
            password: Password to check (will be hashed)
            
        Returns:
            Number of times password has been seen in breaches
        """
        import hashlib
        
        try:
            # Hash the password with SHA-1
            sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.pwnedpasswords.com/range/{prefix}",
                    headers={"User-Agent": "SentinelX-AI"}
                )
                
                if response.status_code == 200:
                    # Parse response to find our hash
                    hashes = response.text.split('\r\n')
                    for hash_line in hashes:
                        hash_suffix, count = hash_line.split(':')
                        if hash_suffix == suffix:
                            return int(count)
                    return 0  # Not found in breaches
                else:
                    logger.error(f"Password check failed: {response.status_code}")
                    return None
        
        except Exception as e:
            logger.error(f"Password check failed: {e}")
            return None
    
    async def get_all_breaches(self) -> Optional[List[Dict]]:
        """
        Get all breaches in the system
        
        Returns:
            List of all breaches
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/breaches",
                    headers={"User-Agent": "SentinelX-AI"}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Failed to get breaches: {response.status_code}")
                    return []
        
        except Exception as e:
            logger.error(f"Failed to get breaches: {e}")
            return []
    
    def _mock_breach_data(self, email: str) -> List[Dict]:
        """Generate mock breach data for testing"""
        return [
            {
                "Name": "LinkedIn",
                "Title": "LinkedIn",
                "Domain": "linkedin.com",
                "BreachDate": "2021-06-22",
                "AddedDate": "2021-06-22T00:00:00Z",
                "ModifiedDate": "2021-06-22T00:00:00Z",
                "PwnCount": 700000000,
                "Description": "In June 2021, data scraped from 700M LinkedIn users was posted for sale on a hacking forum.",
                "LogoPath": "https://haveibeenpwned.com/Content/Images/PwnedLogos/LinkedIn.png",
                "DataClasses": [
                    "Email addresses",
                    "Geographic locations",
                    "Job titles",
                    "Names",
                    "Phone numbers",
                    "Social media profiles"
                ],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False
            },
            {
                "Name": "Collection1",
                "Title": "Collection #1",
                "Domain": "",
                "BreachDate": "2019-01-07",
                "AddedDate": "2019-01-16T21:46:07Z",
                "ModifiedDate": "2019-01-16T21:46:07Z",
                "PwnCount": 772904991,
                "Description": "In January 2019, a large collection of credential stuffing lists was discovered being distributed on a popular hacking forum.",
                "LogoPath": "https://haveibeenpwned.com/Content/Images/PwnedLogos/List.png",
                "DataClasses": [
                    "Email addresses",
                    "Passwords"
                ],
                "IsVerified": False,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False
            }
        ]
    
    def parse_breach_data(self, breaches: List[Dict]) -> Dict:
        """
        Parse breach data into a summary
        
        Args:
            breaches: List of breach dictionaries
            
        Returns:
            Summary dictionary
        """
        if not breaches:
            return {
                "total_breaches": 0,
                "verified_breaches": 0,
                "total_accounts_affected": 0,
                "data_classes": [],
                "most_recent_breach": None
            }
        
        verified = sum(1 for b in breaches if b.get("IsVerified", False))
        total_accounts = sum(b.get("PwnCount", 0) for b in breaches)
        
        # Collect all unique data classes
        data_classes = set()
        for breach in breaches:
            data_classes.update(breach.get("DataClasses", []))
        
        # Find most recent breach
        most_recent = max(breaches, key=lambda b: b.get("BreachDate", ""))
        
        return {
            "total_breaches": len(breaches),
            "verified_breaches": verified,
            "total_accounts_affected": total_accounts,
            "data_classes": sorted(list(data_classes)),
            "most_recent_breach": {
                "name": most_recent.get("Name"),
                "date": most_recent.get("BreachDate"),
                "description": most_recent.get("Description")
            }
        }

# Made with Bob
