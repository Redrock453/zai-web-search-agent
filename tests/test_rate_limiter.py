"""
Tests for rate limiter module
"""

import pytest
import time
import threading
from unittest.mock import patch

from src.agent.rate_limiter import RateLimiter


class TestRateLimiter:
    """
    Test cases for the RateLimiter class
    """
    
    def test_initialization_default_values(self):
        """Test RateLimiter initialization with default values"""
        limiter = RateLimiter()
        
        assert limiter.max_requests == 100
        assert limiter.time_window == 60
        assert limiter.tokens == 100
        assert limiter.last_refill > 0
        assert limiter.lock is not None
    
    def test_initialization_custom_values(self):
        """Test RateLimiter initialization with custom values"""
        limiter = RateLimiter(max_requests=50, time_window=30)
        
        assert limiter.max_requests == 50
        assert limiter.time_window == 30
        assert limiter.tokens == 50
        assert limiter.last_refill > 0
        assert limiter.lock is not None
    
    def test_initialization_invalid_max_requests(self):
        """Test RateLimiter initialization with invalid max_requests"""
        with pytest.raises(ValueError, match="max_requests must be a positive integer"):
            RateLimiter(max_requests=0)
        
        with pytest.raises(ValueError, match="max_requests must be a positive integer"):
            RateLimiter(max_requests=-10)
    
    def test_initialization_invalid_time_window(self):
        """Test RateLimiter initialization with invalid time_window"""
        with pytest.raises(ValueError, match="time_window must be a positive integer"):
            RateLimiter(time_window=0)
        
        with pytest.raises(ValueError, match="time_window must be a positive integer"):
            RateLimiter(time_window=-10)
    
    def test_can_make_request_with_tokens(self):
        """Test can_make_request when tokens are available"""
        limiter = RateLimiter(max_requests=10, time_window=60)
        
        # Should be able to make request initially
        assert limiter.can_make_request() is True
        
        # After consuming a token, should still be able to make request
        limiter.acquire_token()
        assert limiter.can_make_request() is True
    
    def test_can_make_request_without_tokens(self):
        """Test can_make_request when no tokens are available"""
        limiter = RateLimiter(max_requests=2, time_window=60)
        
        # Consume all tokens
        limiter.acquire_token()
        limiter.acquire_token()
        
        # Should not be able to make request
        assert limiter.can_make_request() is False
    
    def test_acquire_token_success(self):
        """Test successful token acquisition"""
        limiter = RateLimiter(max_requests=10, time_window=60)
        
        # Should be able to acquire token
        assert limiter.acquire_token() is True
        assert limiter.get_available_tokens() == 9
    
    def test_acquire_token_failure(self):
        """Test token acquisition when no tokens are available"""
        limiter = RateLimiter(max_requests=2, time_window=60)
        
        # Consume all tokens
        limiter.acquire_token()
        limiter.acquire_token()
        
        # Should not be able to acquire token
        assert limiter.acquire_token() is False
        assert limiter.get_available_tokens() == 0
    
    def test_wait_if_needed_no_wait(self):
        """Test wait_if_needed when no wait is needed"""
        limiter = RateLimiter(max_requests=10, time_window=60)
        
        # Should not wait
        wait_time = limiter.wait_if_needed()
        assert wait_time == 0.0
        assert limiter.get_available_tokens() == 9  # One token consumed
    
    def test_wait_if_needed_with_wait(self):
        """Test wait_if_needed when wait is needed"""
        limiter = RateLimiter(max_requests=2, time_window=1)  # 2 requests per 1 second
        
        # Consume all tokens
        limiter.acquire_token()
        limiter.acquire_token()
        
        # Should wait for next token
        with patch('time.sleep') as mock_sleep:
            wait_time = limiter.wait_if_needed()
            assert wait_time > 0
            mock_sleep.assert_called_once()
    
    def test_get_available_tokens(self):
        """Test get_available_tokens method"""
        limiter = RateLimiter(max_requests=10, time_window=60)
        
        # Initially should have max tokens
        assert limiter.get_available_tokens() == 10
        
        # After consuming tokens
        limiter.acquire_token()
        assert limiter.get_available_tokens() == 9
        
        limiter.acquire_token()
        assert limiter.get_available_tokens() == 8
    
    def test_get_time_until_next_token(self):
        """Test get_time_until_next_token method"""
        limiter = RateLimiter(max_requests=10, time_window=60)
        
        # When tokens are available, should return 0
        assert limiter.get_time_until_next_token() == 0.0
        
        # When no tokens are available, should return positive value
        limiter.acquire_token()
        limiter.acquire_token()
        limiter.acquire_token()
        limiter.acquire_token()
        limiter.acquire_token()
        limiter.acquire_token()
        limiter.acquire_token()
        limiter.acquire_token()
        limiter.acquire_token()
        limiter.acquire_token()  # Consume all tokens
        
        assert limiter.get_time_until_next_token() > 0
    
    def test_reset(self):
        """Test reset method"""
        limiter = RateLimiter(max_requests=10, time_window=60)
        
        # Consume some tokens
        limiter.acquire_token()
        limiter.acquire_token()
        limiter.acquire_token()
        
        assert limiter.get_available_tokens() == 7
        
        # Reset should refill tokens
        limiter.reset()
        assert limiter.get_available_tokens() == 10
    
    def test_token_refill_over_time(self):
        """Test that tokens are refilled over time"""
        limiter = RateLimiter(max_requests=10, time_window=1)  # 10 requests per 1 second
        
        # Consume all tokens
        for _ in range(10):
            limiter.acquire_token()
        
        assert limiter.get_available_tokens() == 0
        
        # Wait for tokens to refill
        time.sleep(1.1)  # Wait slightly more than the time window
        
        # Should have tokens available again
        assert limiter.get_available_tokens() > 0
    
    def test_thread_safety(self):
        """Test that RateLimiter is thread-safe"""
        limiter = RateLimiter(max_requests=100, time_window=60)
        results = []
        
        def worker():
            for _ in range(10):
                if limiter.acquire_token():
                    results.append(1)
                else:
                    results.append(0)
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Total acquired tokens should not exceed max_requests
        total_acquired = sum(results)
        assert total_acquired <= limiter.max_requests
    
    def test_concurrent_wait_if_needed(self):
        """Test concurrent wait_if_needed operations"""
        limiter = RateLimiter(max_requests=1, time_window=1)  # 1 request per 1 second
        results = []
        
        def worker():
            wait_time = limiter.wait_if_needed()
            results.append(wait_time)
        
        # Create multiple threads
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # One thread should not wait, others should wait
        no_waits = sum(1 for t in results if t == 0.0)
        waits = sum(1 for t in results if t > 0.0)
        
        assert no_waits == 1  # Only one thread should not wait
        assert waits == 2     # Two threads should wait
    
    @pytest.mark.parametrize("max_requests,time_window", [
        (1, 1),
        (5, 2),
        (10, 5),
        (100, 60),
    ])
    def test_different_rate_limits(self, max_requests, time_window):
        """Test RateLimiter with different rate limit configurations"""
        limiter = RateLimiter(max_requests=max_requests, time_window=time_window)
        
        # Should be able to make max_requests requests
        for _ in range(max_requests):
            assert limiter.acquire_token() is True
        
        # Should not be able to make more requests
        assert limiter.acquire_token() is False
        
        # Wait for refill
        time.sleep(time_window + 0.1)
        
        # Should be able to make requests again
        assert limiter.acquire_token() is True
    
    def test_refill_tokens_calculation(self):
        """Test token refill calculation"""
        limiter = RateLimiter(max_requests=10, time_window=60)
        
        # Consume all tokens
        for _ in range(10):
            limiter.acquire_token()
        
        assert limiter.get_available_tokens() == 0
        
        # Manually set last_refill to simulate time passing
        with patch('time.time', return_value=limiter.last_refill + 30):  # 30 seconds passed
            # Should have half the tokens (5) after half the time window
            limiter._refill_tokens()
            assert limiter.get_available_tokens() == 5
        
        # Manually set last_refill to simulate full time window passing
        with patch('time.time', return_value=limiter.last_refill + 60):  # 60 seconds passed
            # Should have all tokens after full time window
            limiter._refill_tokens()
            assert limiter.get_available_tokens() == 10