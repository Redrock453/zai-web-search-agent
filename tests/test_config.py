"""
Tests for configuration management
"""

import pytest
import os
import tempfile
from unittest.mock import patch

from src.agent.config import ZAIConfig


class TestZAIConfig:
    """
    Test cases for the ZAIConfig class
    """
    
    def test_default_values(self):
        """Test ZAIConfig with default values"""
        config = ZAIConfig(api_key="zai_test123456789012345678901234567890")
        
        assert config.api_key == "zai_test123456789012345678901234567890"
        assert config.base_url == "https://api.z.ai/v1"
        assert config.timeout == 30
        assert config.max_retries == 3
    
    def test_custom_values(self):
        """Test ZAIConfig with custom values"""
        config = ZAIConfig(
            api_key="zai_custom123456789012345678901234567890",
            base_url="https://custom.api.z.ai/v1",
            timeout=60,
            max_retries=5
        )
        
        assert config.api_key == "zai_custom123456789012345678901234567890"
        assert config.base_url == "https://custom.api.z.ai/v1"
        assert config.timeout == 60
        assert config.max_retries == 5
    
    def test_api_key_validation_valid(self):
        """Test API key validation with valid keys"""
        valid_keys = [
            "zai_abcdefghijklmnopqrstuvwxyz123456",
            "zai_123456789012345678901234567890ab",
            "zai_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"
        ]
        
        for key in valid_keys:
            config = ZAIConfig(api_key=key)
            assert config.api_key == key
    
    def test_api_key_validation_invalid_format(self):
        """Test API key validation with invalid format"""
        invalid_keys = [
            "zai_short",  # Too short
            "zai_123456789012345678901234567890123",  # Too long
            "zai_!@#$%^&*()_+12345678901234567890",  # Invalid characters
            "zai-123456789012345678901234567890",  # Wrong prefix
            "123456789012345678901234567890",  # Missing prefix
            "",  # Empty string
            None  # None value
        ]
        
        for key in invalid_keys:
            with pytest.raises(ValueError, match="Invalid API key format"):
                ZAIConfig(api_key=key)
    
    def test_timeout_validation_valid(self):
        """Test timeout validation with valid values"""
        valid_timeouts = [1, 10, 30, 60, 120]
        
        for timeout in valid_timeouts:
            config = ZAIConfig(
                api_key="zai_test123456789012345678901234567890",
                timeout=timeout
            )
            assert config.timeout == timeout
    
    def test_timeout_validation_invalid(self):
        """Test timeout validation with invalid values"""
        invalid_timeouts = [0, -1, -10]
        
        for timeout in invalid_timeouts:
            with pytest.raises(ValueError, match="Timeout must be a positive integer"):
                ZAIConfig(
                    api_key="zai_test123456789012345678901234567890",
                    timeout=timeout
                )
    
    def test_max_retries_validation_valid(self):
        """Test max_retries validation with valid values"""
        valid_retries = [0, 1, 3, 5, 10]
        
        for retries in valid_retries:
            config = ZAIConfig(
                api_key="zai_test123456789012345678901234567890",
                max_retries=retries
            )
            assert config.max_retries == retries
    
    def test_max_retries_validation_invalid(self):
        """Test max_retries validation with invalid values"""
        invalid_retries = [-1, -10]
        
        for retries in invalid_retries:
            with pytest.raises(ValueError, match="Max retries must be a non-negative integer"):
                ZAIConfig(
                    api_key="zai_test123456789012345678901234567890",
                    max_retries=retries
                )
    
    def test_from_env_with_env_file(self):
        """Test loading configuration from environment file"""
        env_content = """
ZAI_API_KEY=zai_env123456789012345678901234567890
ZAI_BASE_URL=https://env.api.z.ai/v1
ZAI_TIMEOUT=45
ZAI_MAX_RETRIES=7
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write(env_content)
            env_file_path = f.name
        
        try:
            config = ZAIConfig.from_env(env_file=env_file_path)
            
            assert config.api_key == "zai_env123456789012345678901234567890"
            assert config.base_url == "https://env.api.z.ai/v1"
            assert config.timeout == 45
            assert config.max_retries == 7
        finally:
            os.unlink(env_file_path)
    
    def test_from_env_with_os_environment(self):
        """Test loading configuration from OS environment"""
        with patch.dict(os.environ, {
            'ZAI_API_KEY': 'zai_os123456789012345678901234567890',
            'ZAI_BASE_URL': 'https://os.api.z.ai/v1',
            'ZAI_TIMEOUT': '25',
            'ZAI_MAX_RETRIES': '2'
        }):
            config = ZAIConfig.from_env()
            
            assert config.api_key == "zai_os123456789012345678901234567890"
            assert config.base_url == "https://os.api.z.ai/v1"
            assert config.timeout == 25
            assert config.max_retries == 2
    
    def test_from_env_with_defaults(self):
        """Test loading configuration with default values when env vars are missing"""
        with patch.dict(os.environ, {}, clear=True):
            # Should raise ValueError for missing API key
            with pytest.raises(ValueError, match="API key is required"):
                ZAIConfig.from_env()
    
    def test_from_env_with_invalid_api_key(self):
        """Test loading configuration with invalid API key in environment"""
        with patch.dict(os.environ, {
            'ZAI_API_KEY': 'invalid_key',
            'ZAI_TIMEOUT': '30'
        }):
            with pytest.raises(ValueError, match="Invalid API key format"):
                ZAIConfig.from_env()
    
    def test_from_env_with_invalid_timeout(self):
        """Test loading configuration with invalid timeout in environment"""
        with patch.dict(os.environ, {
            'ZAI_API_KEY': 'zai_test123456789012345678901234567890',
            'ZAI_TIMEOUT': 'invalid'
        }):
            with pytest.raises(ValueError):
                ZAIConfig.from_env()
    
    def test_from_env_with_invalid_max_retries(self):
        """Test loading configuration with invalid max_retries in environment"""
        with patch.dict(os.environ, {
            'ZAI_API_KEY': 'zai_test123456789012345678901234567890',
            'ZAI_MAX_RETRIES': 'invalid'
        }):
            with pytest.raises(ValueError):
                ZAIConfig.from_env()
    
    def test_env_priority(self):
        """Test that direct parameters take priority over environment"""
        with patch.dict(os.environ, {
            'ZAI_API_KEY': 'zai_env123456789012345678901234567890',
            'ZAI_BASE_URL': 'https://env.api.z.ai/v1',
            'ZAI_TIMEOUT': '45',
            'ZAI_MAX_RETRIES': '7'
        }):
            config = ZAIConfig(
                api_key="zai_direct123456789012345678901234567890",
                base_url="https://direct.api.z.ai/v1",
                timeout=60,
                max_retries=10
            )
            
            assert config.api_key == "zai_direct123456789012345678901234567890"
            assert config.base_url == "https://direct.api.z.ai/v1"
            assert config.timeout == 60
            assert config.max_retries == 10
    
    @pytest.mark.parametrize("api_key", [
        "zai_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
        "zai_ABCDEF1234567890ABCDEF1234567890",
        "zai_11111111111111111111111111111111"
    ])
    def test_api_key_pattern_matching(self, api_key):
        """Test API key pattern matching with various valid keys"""
        config = ZAIConfig(api_key=api_key)
        assert config.api_key == api_key
    
    def test_config_immutability(self):
        """Test that config attributes can be modified (Pydantic models are mutable by default)"""
        config = ZAIConfig(api_key="zai_test123456789012345678901234567890")
        
        # Modify attributes
        config.base_url = "https://new.api.z.ai/v1"
        config.timeout = 45
        
        assert config.base_url == "https://new.api.z.ai/v1"
        assert config.timeout == 45