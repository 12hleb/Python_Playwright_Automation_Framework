"""
API tests for JSONPlaceholder API.
"""

import pytest
from api.jsonplaceholder_api import JSONPlaceholderAPI


@pytest.mark.api
@pytest.mark.smoke
class TestJSONPlaceholderAPI:
    """Test cases for JSONPlaceholder API."""
    
    @pytest.fixture(scope="class")
    def api_client(self):
        """Create API client instance."""
        return JSONPlaceholderAPI()
        
    def test_get_all_posts(self, api_client):
        """Test getting all posts."""
        posts = api_client.get_posts()
        
        # Verify response
        assert isinstance(posts, list)
        assert len(posts) == 100  # JSONPlaceholder has 100 posts
        
        # Verify post structure
        first_post = posts[0]
        assert "id" in first_post
        assert "title" in first_post
        assert "body" in first_post
        assert "userId" in first_post
        
    def test_get_posts_by_user(self, api_client):
        """Test getting posts by specific user."""
        user_id = 1
        posts = api_client.get_posts(user_id=user_id)
        
        # Verify all posts belong to the user
        assert isinstance(posts, list)
        assert len(posts) > 0
        
        for post in posts:
            assert post["userId"] == user_id
            
    def test_get_single_post(self, api_client):
        """Test getting a single post by ID."""
        post_id = 1
        post = api_client.get_post(post_id)
        
        # Verify post data
        assert post["id"] == post_id
        assert "title" in post
        assert "body" in post
        assert "userId" in post
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)
        
    def test_create_post(self, api_client):
        """Test creating a new post."""
        new_post_data = {
            "title": "Test Post",
            "body": "This is a test post created by automation",
            "userId": 1
        }
        
        created_post = api_client.create_post(
            title=new_post_data["title"],
            body=new_post_data["body"],
            user_id=new_post_data["userId"]
        )
        
        # Verify created post
        assert created_post["title"] == new_post_data["title"]
        assert created_post["body"] == new_post_data["body"]
        assert created_post["userId"] == new_post_data["userId"]
        assert "id" in created_post
        
    def test_update_post(self, api_client):
        """Test updating an existing post."""
        post_id = 1
        updated_data = {
            "title": "Updated Test Post",
            "body": "This post has been updated",
            "userId": 1
        }
        
        updated_post = api_client.update_post(
            post_id=post_id,
            title=updated_data["title"],
            body=updated_data["body"],
            user_id=updated_data["userId"]
        )
        
        # Verify updated post
        assert updated_post["id"] == post_id
        assert updated_post["title"] == updated_data["title"]
        assert updated_post["body"] == updated_data["body"]
        assert updated_post["userId"] == updated_data["userId"]
        
    def test_patch_post(self, api_client):
        """Test partially updating a post."""
        post_id = 1
        patch_data = {"title": "Patched Title"}
        
        patched_post = api_client.patch_post(post_id, **patch_data)
        
        # Verify patched post
        assert patched_post["id"] == post_id
        assert patched_post["title"] == patch_data["title"]
        # Other fields should remain unchanged
        assert "body" in patched_post
        assert "userId" in patched_post
        
    def test_delete_post(self, api_client):
        """Test deleting a post."""
        post_id = 1
        
        # Delete should not raise an exception
        api_client.delete_post(post_id)
        
    def test_get_all_users(self, api_client):
        """Test getting all users."""
        users = api_client.get_users()
        
        # Verify response
        assert isinstance(users, list)
        assert len(users) == 10  # JSONPlaceholder has 10 users
        
        # Verify user structure
        first_user = users[0]
        required_fields = ["id", "name", "username", "email"]
        for field in required_fields:
            assert field in first_user
            
    def test_get_single_user(self, api_client):
        """Test getting a single user by ID."""
        user_id = 1
        user = api_client.get_user(user_id)
        
        # Verify user data
        assert user["id"] == user_id
        assert "name" in user
        assert "username" in user
        assert "email" in user
        assert "address" in user
        assert "company" in user
        
    def test_get_comments(self, api_client):
        """Test getting comments."""
        comments = api_client.get_comments()
        
        # Verify response
        assert isinstance(comments, list)
        assert len(comments) > 0
        
        # Verify comment structure
        first_comment = comments[0]
        required_fields = ["id", "name", "email", "body", "postId"]
        for field in required_fields:
            assert field in first_comment
            
    def test_get_comments_by_post(self, api_client):
        """Test getting comments for a specific post."""
        post_id = 1
        comments = api_client.get_comments(post_id=post_id)
        
        # Verify all comments belong to the post
        assert isinstance(comments, list)
        assert len(comments) > 0
        
        for comment in comments:
            assert comment["postId"] == post_id
            
    def test_get_albums(self, api_client):
        """Test getting albums."""
        albums = api_client.get_albums()
        
        # Verify response
        assert isinstance(albums, list)
        assert len(albums) > 0
        
        # Verify album structure
        first_album = albums[0]
        required_fields = ["id", "title", "userId"]
        for field in required_fields:
            assert field in first_album
            
    def test_get_photos(self, api_client):
        """Test getting photos."""
        photos = api_client.get_photos()
        
        # Verify response
        assert isinstance(photos, list)
        assert len(photos) > 0
        
        # Verify photo structure
        first_photo = photos[0]
        required_fields = ["id", "title", "url", "thumbnailUrl", "albumId"]
        for field in required_fields:
            assert field in first_photo
            
    @pytest.mark.slow
    def test_api_response_times(self, api_client):
        """Test API response times are reasonable."""
        import time
        
        # Test multiple endpoints for performance
        endpoints_to_test = [
            lambda: api_client.get_posts(),
            lambda: api_client.get_users(),
            lambda: api_client.get_comments(),
        ]
        
        for endpoint in endpoints_to_test:
            start_time = time.time()
            endpoint()
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to ms
            assert response_time < 2000, f"API response took too long: {response_time}ms" 