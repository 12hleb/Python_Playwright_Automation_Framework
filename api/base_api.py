"""
Base API client for API testing.
"""

import requests
from typing import Dict, Any, Optional
from loguru import logger


class BaseAPI:
    """Base API client for making HTTP requests."""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """Initialize API client."""
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Playwright-API-Tests/1.0'
        })
        
    def set_auth_token(self, token: str) -> None:
        """Set authorization token."""
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        
    def set_header(self, key: str, value: str) -> None:
        """Set a custom header."""
        self.session.headers.update({key: value})
        
    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """Make GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"GET request to: {url}")
        
        response = self.session.get(url, params=params, timeout=self.timeout)
        logger.info(f"Response status: {response.status_code}")
        return response
        
    def post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> requests.Response:
        """Make POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"POST request to: {url}")
        
        response = self.session.post(url, data=data, json=json, timeout=self.timeout)
        logger.info(f"Response status: {response.status_code}")
        return response
        
    def put(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> requests.Response:
        """Make PUT request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"PUT request to: {url}")
        
        response = self.session.put(url, data=data, json=json, timeout=self.timeout)
        logger.info(f"Response status: {response.status_code}")
        return response
        
    def patch(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> requests.Response:
        """Make PATCH request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"PATCH request to: {url}")
        
        response = self.session.patch(url, data=data, json=json, timeout=self.timeout)
        logger.info(f"Response status: {response.status_code}")
        return response
        
    def delete(self, endpoint: str) -> requests.Response:
        """Make DELETE request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"DELETE request to: {url}")
        
        response = self.session.delete(url, timeout=self.timeout)
        logger.info(f"Response status: {response.status_code}")
        return response
        
    def assert_status_code(self, response: requests.Response, expected_code: int) -> None:
        """Assert response status code."""
        assert response.status_code == expected_code, \
            f"Expected status code {expected_code}, got {response.status_code}. Response: {response.text}"
            
    def assert_response_contains(self, response: requests.Response, key: str) -> None:
        """Assert response contains specific key."""
        response_json = response.json()
        assert key in response_json, f"Key '{key}' not found in response: {response_json}"
        
    def get_json_value(self, response: requests.Response, key: str) -> Any:
        """Get value from JSON response."""
        response_json = response.json()
        return response_json.get(key)
        
    def close(self) -> None:
        """Close the session."""
        self.session.close() 