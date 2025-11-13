"""
Comprehensive tests for the WebSearchAgent class
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
import time

from src.agent.web_search_agent import WebSearchAgent
from src.agent.config import ZAIConfig
from src.agent.auth import ZAIAuthenticator
from src.agent.models import SearchRequest, SearchResponse, SearchResult
from src.agent.exceptions import (
    ZAIApiError,
    ZAIAuthenticationError,
    ZAIRateLimitError,
    ZAIInvalidRequestError,
    ZAIServerError
)


class TestWebSearchAgent:
    """
    Test cases for the WebSearchAgent class
    """
    
    @pytest.fixture
    def mock_config(self):
        """Create a mock ZAIConfig for testing"""
        return ZAIConfig(
            api_key="zai_test123456789012345678901234567890",
            base_url="https://api.test.z.ai/v1",
            timeout=30,
            max_retries=3
        )
    
    @pytest.fixture
    def mock_authenticator(self):
        """Create a mock ZAIAuthenticator for testing"""
        auth = Mock(spec=ZAIAuthenticator)
        auth.get_auth_headers.return_value = {
            "Authorization": "Bearer zai_test123456789012345678901234567890",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return auth
    
    @pytest.fixture
    def agent(self, mock_config, mock_authenticator):
        """Create a WebSearchAgent instance for testing"""
        return WebSearchAgent(
            config=mock_config,
            authenticator=mock_authenticator,
            max_retries=2,
            initial_backoff=0.1,
            max_backoff=1.0,
            rate_limit_requests=10,
            rate_limit_window=60
        )
    
    @pytest.fixture
    def sample_api_response(self):
        """Sample API response for testing"""
        return {
            "results": [
                {
                    "title": "Test Result 1",
                    "url": "https://example.com/1",
                    "snippet": "This is a test snippet",
                    "position": 1
                },
                {
                    "title": "Test Result 2",
                    "url": "https://example.com/2",
                    "snippet": "This is another test snippet",
                    "position": 2
                }
            ],
            "total_results": 2,
            "search_time": 0.5,
            "has_more": False
        }
    
    def test_initialization_with_config_and_auth(self, mock_config, mock_authenticator):
        """Test WebSearchAgent initialization with config and authenticator"""
        agent = WebSearchAgent(config=mock_config, authenticator=mock_authenticator)
        
        assert agent.config == mock_config
        assert agent.authenticator == mock_authenticator
        assert agent.max_retries == 3
        assert agent.initial_backoff == 1.0
        assert agent.max_backoff == 60.0
        assert agent.search_endpoint == "https://api.test.z.ai/v1/search"
        assert agent.rate_limiter is not None
    
    def test_initialization_with_api_key(self, mock_config):
        """Test WebSearchAgent initialization with API key"""
        agent = WebSearchAgent(config=mock_config, api_key="zai_new123456789012345678901234567890")
        
        assert agent.config == mock_config
        assert agent.authenticator is not None
        assert agent.authenticator.api_key == "zai_new123456789012345678901234567890"
    
    def test_initialization_without_credentials(self):
        """Test WebSearchAgent initialization without credentials for testing"""
        agent = WebSearchAgent()
        
        assert agent.config is not None
        assert agent.authenticator is None  # Should be None for testing
    
    def test_search_with_parameters(self, agent, sample_api_response):
        """Test search method with various parameters"""
        with patch.object(agent, '_make_request_with_retry', return_value=sample_api_response):
            response = agent.search(
                query="test query",
                num_results=5,
                include_domains=["example.com"],
                exclude_domains=["spam.com"],
                search_type="news",
                language="en",
                region="us",
                safe_search="strict"
            )
            
            assert isinstance(response, SearchResponse)
            assert response.query == "test query"
            assert response.search_type == "news"
            assert len(response.results) == 2
            assert response.results[0].title == "Test Result 1"
            assert response.results[0].url == "https://example.com/1"
            assert response.results[0].domain == "example.com"
    
    def test_search_with_request_model(self, agent, sample_api_response):
        """Test search_with_request method with SearchRequest model"""
        request = SearchRequest(
            query="test query",
            num_results=10,
            search_type="web"
        )
        
        with patch.object(agent, '_make_request_with_retry', return_value=sample_api_response):
            response = agent.search_with_request(request)
            
            assert isinstance(response, SearchResponse)
            assert response.query == "test query"
            assert response.search_type == "web"
    
    @patch('requests.get')
    def test_make_request_success(self, mock_get, agent, sample_api_response):
        """Test successful API request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_api_response
        mock_get.return_value = mock_response
        
        result = agent._make_request("https://api.test.z.ai/v1/search", {"query": "test"})
        
        assert result == sample_api_response
        mock_get.assert_called_once()
    
    @patch('requests.get')
    def test_make_request_authentication_error(self, mock_get, agent):
        """Test API request with authentication error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.content = b'{"error": "Invalid API key"}'
        mock_get.return_value = mock_response
        
        with pytest.raises(ZAIAuthenticationError):
            agent._make_request("https://api.test.z.ai/v1/search", {"query": "test"})
    
    @patch('requests.get')
    def test_make_request_rate_limit_error(self, mock_get, agent):
        """Test API request with rate limit error"""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b'{"error": "Rate limit exceeded", "retry_after": 5}'
        mock_get.return_value = mock_response
        
        with pytest.raises(ZAIRateLimitError) as exc_info:
            agent._make_request("https://api.test.z.ai/v1/search", {"query": "test"})
        
        assert exc_info.value.response_data["retry_after"] == 5
    
    @patch('requests.get')
    def test_make_request_invalid_request_error(self, mock_get, agent):
        """Test API request with invalid request error"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.content = b'{"error": "Invalid parameters"}'
        mock_get.return_value = mock_response
        
        with pytest.raises(ZAIInvalidRequestError):
            agent._make_request("https://api.test.z.ai/v1/search", {"query": "test"})
    
    @patch('requests.get')
    def test_make_request_server_error(self, mock_get, agent):
        """Test API request with server error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.content = b'{"error": "Internal server error"}'
        mock_get.return_value = mock_response
        
        with pytest.raises(ZAIServerError):
            agent._make_request("https://api.test.z.ai/v1/search", {"query": "test"})
    
    @patch('requests.get')
    def test_make_request_timeout(self, mock_get, agent):
        """Test API request with timeout"""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        with pytest.raises(ZAIApiError) as exc_info:
            agent._make_request("https://api.test.z.ai/v1/search", {"query": "test"})
        
        assert "timed out" in str(exc_info.value)
    
    @patch('requests.get')
    def test_make_request_connection_error(self, mock_get, agent):
        """Test API request with connection error"""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        with pytest.raises(ZAIApiError) as exc_info:
            agent._make_request("https://api.test.z.ai/v1/search", {"query": "test"})
        
        assert "Failed to connect" in str(exc_info.value)
    
    def test_make_request_with_retry_success(self, agent, sample_api_response):
        """Test _make_request_with_retry with successful request"""
        with patch.object(agent, '_make_request', return_value=sample_api_response):
            with patch.object(agent.rate_limiter, 'wait_if_needed', return_value=0):
                result = agent._make_request_with_retry("https://api.test.z.ai/v1/search", {"query": "test"})
                
                assert result == sample_api_response
                agent.rate_limiter.wait_if_needed.assert_called_once()
    
    def test_make_request_with_retry_rate_limit_with_retry_after(self, agent):
        """Test _make_request_with_retry with rate limit error and retry-after header"""
        # First call raises rate limit error with retry_after
        rate_limit_error = ZAIRateLimitError(
            "Rate limit exceeded",
            response_data={"retry_after": 0.1}
        )
        
        # Second call succeeds
        sample_response = {"results": []}
        
        with patch.object(agent, '_make_request') as mock_request:
            with patch.object(agent.rate_limiter, 'wait_if_needed', return_value=0):
                with patch('time.sleep') as mock_sleep:
                    mock_request.side_effect = [rate_limit_error, sample_response]
                    
                    result = agent._make_request_with_retry("https://api.test.z.ai/v1/search", {"query": "test"})
                    
                    assert result == sample_response
                    assert mock_request.call_count == 2
                    mock_sleep.assert_called_with(0.1)
    
    def test_make_request_with_retry_rate_limit_exponential_backoff(self, agent):
        """Test _make_request_with_retry with rate limit error using exponential backoff"""
        # First call raises rate limit error without retry_after
        rate_limit_error = ZAIRateLimitError("Rate limit exceeded")
        
        # Second call succeeds
        sample_response = {"results": []}
        
        with patch.object(agent, '_make_request') as mock_request:
            with patch.object(agent.rate_limiter, 'wait_if_needed', return_value=0):
                with patch('time.sleep') as mock_sleep:
                    mock_request.side_effect = [rate_limit_error, sample_response]
                    
                    result = agent._make_request_with_retry("https://api.test.z.ai/v1/search", {"query": "test"})
                    
                    assert result == sample_response
                    assert mock_request.call_count == 2
                    mock_sleep.assert_called_with(0.1)  # initial_backoff
    
    def test_make_request_with_retry_max_retries_exceeded(self, agent):
        """Test _make_request_with_retry when max retries is exceeded"""
        api_error = ZAIApiError("Server error")
        
        with patch.object(agent, '_make_request', side_effect=api_error):
            with patch.object(agent.rate_limiter, 'wait_if_needed', return_value=0):
                with patch('time.sleep'):
                    with pytest.raises(ZAIApiError):
                        agent._make_request_with_retry("https://api.test.z.ai/v1/search", {"query": "test"})
    
    def test_make_request_with_retry_no_retry_for_auth_error(self, agent):
        """Test _make_request_with_retry doesn't retry authentication errors"""
        auth_error = ZAIAuthenticationError("Invalid API key")
        
        with patch.object(agent, '_make_request', side_effect=auth_error):
            with patch.object(agent.rate_limiter, 'wait_if_needed', return_value=0):
                with pytest.raises(ZAIAuthenticationError):
                    agent._make_request_with_retry("https://api.test.z.ai/v1/search", {"query": "test"})
    
    def test_make_request_with_retry_no_retry_for_invalid_request_error(self, agent):
        """Test _make_request_with_retry doesn't retry invalid request errors"""
        invalid_error = ZAIInvalidRequestError("Invalid parameters")
        
        with patch.object(agent, '_make_request', side_effect=invalid_error):
            with patch.object(agent.rate_limiter, 'wait_if_needed', return_value=0):
                with pytest.raises(ZAIInvalidRequestError):
                    agent._make_request_with_retry("https://api.test.z.ai/v1/search", {"query": "test"})
    
    def test_transform_api_response(self, agent):
        """Test _transform_api_response method"""
        api_response = {
            "results": [
                {
                    "title": "Test Result",
                    "url": "https://example.com/test",
                    "snippet": "Test snippet",
                    "position": 1,
                    "published_date": "2023-01-01",
                    "thumbnail_url": "https://example.com/image.jpg"
                }
            ],
            "total_results": 1,
            "search_time": 0.5,
            "has_more": True,
            "next_page_token": "abc123"
        }
        
        request = SearchRequest(query="test", search_type="web")
        
        response = agent._transform_api_response(api_response, request)
        
        assert isinstance(response, SearchResponse)
        assert response.query == "test"
        assert response.search_type == "web"
        assert response.total_results == 1
        assert response.search_time == 0.5
        assert response.has_more is True
        assert response.next_page_token == "abc123"
        assert len(response.results) == 1
        
        result = response.results[0]
        assert isinstance(result, SearchResult)
        assert result.title == "Test Result"
        assert result.url == "https://example.com/test"
        assert result.snippet == "Test snippet"
        assert result.position == 1
        assert result.domain == "example.com"
        assert result.published_date == "2023-01-01"
        assert result.thumbnail_url == "https://example.com/image.jpg"
    
    def test_transform_api_response_minimal(self, agent):
        """Test _transform_api_response with minimal data"""
        api_response = {
            "results": [
                {
                    "title": "Test",
                    "url": "https://example.com",
                    "snippet": "Snippet",
                    "position": 1
                }
            ]
        }
        
        request = SearchRequest(query="test", search_type="web")
        
        response = agent._transform_api_response(api_response, request)
        
        assert response.total_results == 1  # Default to length of results
        assert response.search_time == 0.0  # Default value
        assert response.has_more is False  # Default value
        assert response.next_page_token is None  # Default value
        
        result = response.results[0]
        assert result.domain == "example.com"
        assert result.published_date is None
        assert result.thumbnail_url is None
    
    @pytest.mark.parametrize("query,num_results,search_type,language,region,safe_search", [
        ("test query", 10, "web", None, None, "moderate"),
        ("news search", 5, "news", "en", "us", "strict"),
        ("image search", 15, "images", "fr", "fr", "off"),
    ])
    def test_search_parameterized(self, agent, sample_api_response, query, num_results, search_type, language, region, safe_search):
        """Test search method with parameterized inputs"""
        with patch.object(agent, '_make_request_with_retry', return_value=sample_api_response):
            response = agent.search(
                query=query,
                num_results=num_results,
                search_type=search_type,
                language=language,
                region=region,
                safe_search=safe_search
            )
            
            assert isinstance(response, SearchResponse)
            assert response.query == query
            assert response.search_type == search_type