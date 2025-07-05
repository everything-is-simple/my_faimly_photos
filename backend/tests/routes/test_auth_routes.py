import pytest
from app.models import User
from app import db

class TestRegister:
    """Test case for the /api/auth/register endpoint."""

    def test_register_success(self, test_client, init_database):
        """
        GIVEN a POST request to /api/auth/register with valid data
        WHEN the request is processed
        THEN it should return a 201 status code and the new user's data
        """
        response = test_client.post('/api/auth/register', json={
            'username': 'testuser',
            'password': 'password123'
        })
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['code'] == 201
        assert json_data['message'] == 'User registered successfully.'
        assert 'user' in json_data['data']
        assert json_data['data']['user']['username'] == 'testuser'

    def test_register_username_taken(self, test_client, init_database):
        """
        GIVEN a username that already exists in the database
        WHEN a POST request is made to /api/auth/register with the same username
        THEN it should return a 422 status code
        """
        # First, create a user
        test_client.post('/api/auth/register', json={
            'username': 'existinguser',
            'password': 'password123'
        })
        # Then, try to register with the same username
        response = test_client.post('/api/auth/register', json={
            'username': 'existinguser',
            'password': 'password456'
        })
        assert response.status_code == 422
        json_data = response.get_json()
        assert json_data['code'] == 422
        assert 'username' in json_data['data']['errors']

    def test_register_missing_username(self, test_client, init_database):
        """
        GIVEN a POST request to /api/auth/register with no username
        WHEN the request is processed
        THEN it should return a 422 status code
        """
        response = test_client.post('/api/auth/register', json={
            'password': 'password123'
        })
        assert response.status_code == 422
        json_data = response.get_json()
        assert json_data['code'] == 422
        assert 'username' in json_data['data']['errors']

    def test_register_missing_password(self, test_client, init_database):
        """
        GIVEN a POST request to /api/auth/register with no password
        WHEN the request is processed
        THEN it should return a 422 status code
        """
        response = test_client.post('/api/auth/register', json={
            'username': 'testuser'
        })
        assert response.status_code == 422
        json_data = response.get_json()
        assert json_data['code'] == 422
        assert 'password' in json_data['data']['errors']

    def test_password_is_hashed(self, test_client, init_database):
        """
        GIVEN a successful user registration
        WHEN the user is retrieved from the database
        THEN the password_hash should not be the plain text password
        """
        original_password = 'a-very-secure-password'
        test_client.post('/api/auth/register', json={
            'username': 'hashuser',
            'password': original_password
        })

        # Using a direct db session to check the stored data
        user = User.query.filter_by(username='hashuser').first()
        assert user is not None
        assert user.password_hash != original_password
        assert user.password_hash is not None 