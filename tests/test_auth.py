"""
Tests for authentication module
"""

import pytest
from unittest.mock import Mock

from src.agent.auth import ZAIAuthenticator
from src.agent.config import ZAIConfig
from src.agent.exceptions import ZAIAuthenticationError, ZAIInvalidRequestError


class TestZAIAuthenticator:
    """
    Test cases for the ZAIAuthenticator class
    """
    
    @pytest.fixture
    def valid_api_key(self):
        """A valid API key for testing"""
        return "zai_test123456789012345678901234567890"
    
    @pytest.fixture
    def invalid_api_key(self):
        """An invalid API key for testing"""
        return "invalid_key"
    
    @pytest.fixture
    def mock_config(self, valid_api_key):
        """A mock ZAIConfig with a valid API key"""
        return ZAIConfig(
            api_key=valid_api_key,
            base_url="https://api.test.z.ai/v1"
        )
    
    def test_init_with_api_key(self, valid_api_key):
        """Test ZAIAuthenticator initialization with API key"""
        auth = ZAIAuthenticator(api_key=valid_api_key)
        
        assert auth.api_key == valid_api_key
        assert auth.config is None
    
    def test_init_with_config(self, mock_config):
        """Test ZAIAuthenticator initialization with config"""
        auth = ZAIAuthenticator(config=mock_config)
        
        assert auth.api_key == mock_config.api_key
        assert auth.config == mock_config
    
    def test_init_with_api_key_overrides_config(self, mock_config, valid_api_key):
        """Test that API key parameter overrides config API key"""
        different_key = "zai_different123456789012345678901234567890"
        auth = ZAIAuthenticator(config=mock_config, api_key=different_key)
        
        assert auth.api_key == different_key
        assert auth.config == mock_config
    
    def test_init_without_credentials(self):
        """Test ZAIAuthenticator initialization without credentials"""
        with pytest.raises(ZAIAuthenticationError, match="API key is required"):
            ZAIAuthenticator()
    
    def test_init_with_empty_api_key(self):
        """Test ZAIAuthenticator initialization with empty API key"""
        with pytest.raises(ZAIAuthenticationError, match="API key is required"):
            ZAIAuthenticator(api_key="")
    
    def test_init_with_config_without_api_key(self):
        """Test ZAIAuthenticator initialization with config that has no API key"""
        config = ZAIConfig(
            api_key="",
            base_url="https://api.test.z.ai/v1"
        )
        
        with pytest.raises(ZAIAuthenticationError, match="API key is required"):
            ZAIAuthenticator(config=config)
    
    def test_init_with_invalid_api_key_format(self, invalid_api_key):
        """Test ZAIAuthenticator initialization with invalid API key format"""
        with pytest.raises(ZAIInvalidRequestError, match="Invalid API key format"):
            ZAIAuthenticator(api_key=invalid_api_key)
    
    def test_init_with_config_invalid_api_key(self, invalid_api_key):
        """Test ZAIAuthenticator initialization with config containing invalid API key"""
        config = ZAIConfig(
            api_key=invalid_api_key,
            base_url="https://api.test.z.ai/v1"
        )
        
        with pytest.raises(ZAIInvalidRequestError, match="Invalid API key format"):
            ZAIAuthenticator(config=config)
    
    def test_get_auth_headers(self, valid_api_key):
        """Test get_auth_headers returns correct headers"""
        auth = ZAIAuthenticator(api_key=valid_api_key)
        headers = auth.get_auth_headers()
        
        assert headers["Authorization"] == f"Bearer {valid_api_key}"
        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"
    
    def test_validate_credentials_valid(self, valid_api_key):
        """Test validate_credentials with valid credentials"""
        auth = ZAIAuthenticator(api_key=valid_api_key)
        result = auth.validate_credentials()
        
        assert result is True
    
    def test_validate_credentials_invalid_format(self, invalid_api_key):
        """Test validate_credentials with invalid API key format"""
        # We need to create the authenticator first with a valid key
        auth = ZAIAuthenticator(api_key="zai_test123456789012345678901234567890")
        # Then manually set the invalid key to test validation
        auth.api_key = invalid_api_key
        
        with pytest.raises(ZAIAuthenticationError, match="Invalid credentials"):
            auth.validate_credentials()
    
    def test_validate_credentials_empty(self):
        """Test validate_credentials with empty API key"""
        # We need to create the authenticator first with a valid key
        auth = ZAIAuthenticator(api_key="zai_test123456789012345678901234567890")
        # Then manually set an empty key to test validation
        auth.api_key = ""
        
        with pytest.raises(ZAIAuthenticationError, match="Invalid credentials"):
            auth.validate_credentials()
    
    def test_from_api_key(self, valid_api_key):
        """Test from_api_key class method"""
        auth = ZAIAuthenticator.from_api_key(valid_api_key)
        
        assert isinstance(auth, ZAIAuthenticator)
        assert auth.api_key == valid_api_key
        assert auth.config is None
    
    def test_from_api_key_invalid(self, invalid_api_key):
        """Test from_api_key class method with invalid API key"""
        with pytest.raises(ZAIInvalidRequestError, match="Invalid API key format"):
            ZAIAuthenticator.from_api_key(invalid_api_key)
    
    def test_from_config(self, mock_config):
        """Test from_config class method"""
        auth = ZAIAuthenticator.from_config(mock_config)
        
        assert isinstance(auth, ZAIAuthenticator)
        assert auth.api_key == mock_config.api_key
        assert auth.config == mock_config
    
    def test_from_config_invalid_api_key(self, invalid_api_key):
        """Test from_config class method with config containing invalid API key"""
        config = ZAIConfig(
            api_key=invalid_api_key,
            base_url="https://api.test.z.ai/v1"
        )
        
        with pytest.raises(ZAIInvalidRequestError, match="Invalid API key format"):
            ZAIAuthenticator.from_config(config)
    
    def test_api_key_pattern_validation(self):
        """Test API key pattern validation with various formats"""
        valid_keys = [
            "zai_abcdefghijklmnopqrstuvwxyz123456",
            "zai_123456789012345678901234567890ab",
            "zai_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
            "zai_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
        ]
        
        for key in valid_keys:
            auth = ZAIAuthenticator(api_key=key)
            assert auth.api_key == key
    
    def test_get_auth_headers_exception(self):
        """Test get_auth_headers when an exception occurs"""
        # Create a mock that raises an exception when accessing api_key
        class MockAuth:
            def __init__(self):
                self.api_key = "zai_test123456789012345678901234567890"
            
            def get_auth_headers(self):
                # Simulate an exception
                raise Exception("Test exception")
        
        mock_auth = MockAuth()
        # Replace the method with ZAIAuthenticator's method
        mock_auth.get_auth_headers = ZAIAuthenticator.get_auth_headers.__get__(mock_auth)
        
        with pytest.raises(ZAIAuthenticationError, match="Failed to generate auth headers"):
            mock_auth.get_auth_headers()
    
    @pytest.mark.parametrize("api_key", [
        "zai_short",  # Too short
        "zai_123456789012345678901234567890123",  # Too long
        "zai_!@#$%^&*()_+12345678901234567890",  # Invalid characters
        "zai-123456789012345678901234567890",  # Wrong prefix
        "123456789012345678901234567890",  # Missing prefix
    ])
    def test_validate_api_key_invalid_formats(self, api_key):
        """Test _validate_api_key with various invalid formats"""
        # We need to create the authenticator first with a valid key
        auth = ZAIAuthenticator(api_key="zai_test123456789012345678901234567890")
        # Then test the validation method directly
        with pytest.raises(ZAIInvalidRequestError, match="Invalid API key format"):
            auth._validate_api_key(api_key)
    
    def test_validate_api_key_empty(self):
        """Test _validate_api_key with empty API key"""
        # We need to create the authenticator first with a valid key
        auth = ZAIAuthenticator(api_key="zai_test123456789012345678901234567890")
        # Then test the validation method directly
        with pytest.raises(ZAIInvalidRequestError, match="API key cannot be empty"):
            auth._validate_api_key("")
