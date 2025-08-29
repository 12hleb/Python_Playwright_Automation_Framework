"""
JSONPlaceholder API client for testing.
"""

from typing import List, Dict, Any
from .base_api import BaseAPI


class JSONPlaceholderAPI(BaseAPI):
    """API client for JSONPlaceholder test API."""
    
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        """Initialize JSONPlaceholder API client."""
        super().__init__(base_url)
        
    def get_posts(self, user_id: int = None) -> List[Dict[str, Any]]:
        """Get all posts or posts by user ID."""
        params = {"userId": user_id} if user_id else None
        response = self.get("/posts", params=params)
        self.assert_status_code(response, 200)
        return response.json()
        
    def get_post(self, post_id: int) -> Dict[str, Any]:
        """Get a specific post by ID."""
        response = self.get(f"/posts/{post_id}")
        self.assert_status_code(response, 200)
        return response.json()
        
    def create_post(self, title: str, body: str, user_id: int) -> Dict[str, Any]:
        """Create a new post."""
        data = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        response = self.post("/posts", json=data)
        self.assert_status_code(response, 201)
        return response.json()
        
    def update_post(self, post_id: int, title: str, body: str, user_id: int) -> Dict[str, Any]:
        """Update an existing post."""
        data = {
            "id": post_id,
            "title": title,
            "body": body,
            "userId": user_id
        }
        response = self.put(f"/posts/{post_id}", json=data)
        self.assert_status_code(response, 200)
        return response.json()
        
    def patch_post(self, post_id: int, **kwargs) -> Dict[str, Any]:
        """Partially update a post."""
        response = self.patch(f"/posts/{post_id}", json=kwargs)
        self.assert_status_code(response, 200)
        return response.json()
        
    def delete_post(self, post_id: int) -> None:
        """Delete a post."""
        response = self.delete(f"/posts/{post_id}")
        self.assert_status_code(response, 200)
        
    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        response = self.get("/users")
        self.assert_status_code(response, 200)
        return response.json()
        
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get a specific user by ID."""
        response = self.get(f"/users/{user_id}")
        self.assert_status_code(response, 200)
        return response.json()
        
    def get_comments(self, post_id: int = None) -> List[Dict[str, Any]]:
        """Get all comments or comments for a specific post."""
        params = {"postId": post_id} if post_id else None
        response = self.get("/comments", params=params)
        self.assert_status_code(response, 200)
        return response.json()
        
    def get_albums(self, user_id: int = None) -> List[Dict[str, Any]]:
        """Get all albums or albums by user ID."""
        params = {"userId": user_id} if user_id else None
        response = self.get("/albums", params=params)
        self.assert_status_code(response, 200)
        return response.json()
        
    def get_photos(self, album_id: int = None) -> List[Dict[str, Any]]:
        """Get all photos or photos from a specific album."""
        params = {"albumId": album_id} if album_id else None
        response = self.get("/photos", params=params)
        self.assert_status_code(response, 200)
        return response.json() 