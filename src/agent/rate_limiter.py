"""
Rate limiter implementation using token bucket algorithm for Z.AI API requests
"""

import time
import threading
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Rate limiter implementation using the token bucket algorithm.
    
    This class ensures that API requests do not exceed the specified rate limit
    by using a token bucket algorithm. It's thread-safe for concurrent requests.
    
    Attributes:
        max_requests: Maximum number of requests allowed in the time window
        time_window: Time window in seconds (default: 60 for per-minute limits)
        tokens: Current number of available tokens
        last_refill: Timestamp of the last token refill
        lock: Thread lock for thread safety
    """
    
    def __init__(self, max_requests: int = 100, time_window: int = 60):
        """
        Initialize the rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in the time window (default: 100)
            time_window: Time window in seconds (default: 60 for per-minute limits)
        """
        if max_requests <= 0:
            raise ValueError("max_requests must be a positive integer")
        if time_window <= 0:
            raise ValueError("time_window must be a positive integer")
            
        self.max_requests = max_requests
        self.time_window = time_window
        self.tokens = max_requests  # Start with a full bucket
        self.last_refill = time.time()
        self.lock = threading.Lock()
        
        logger.debug(f"RateLimiter initialized: {max_requests} requests per {time_window} seconds")
    
    def _refill_tokens(self) -> None:
        """
        Refill tokens based on elapsed time since last refill.
        
        This method should be called within a lock to ensure thread safety.
        """
        current_time = time.time()
        elapsed_time = current_time - self.last_refill
        
        # Calculate how many tokens to add based on elapsed time
        tokens_to_add = elapsed_time * (self.max_requests / self.time_window)
        
        # Update tokens and last_refill time
        self.tokens = min(self.max_requests, self.tokens + tokens_to_add)
        self.last_refill = current_time
        
        logger.debug(f"Refilled tokens: {self.tokens:.2f} available")
    
    def can_make_request(self) -> bool:
        """
        Check if a request can be made without waiting.
        
        Returns:
            True if a request can be made immediately, False otherwise
        """
        with self.lock:
            self._refill_tokens()
            return self.tokens >= 1
    
    def wait_if_needed(self) -> float:
        """
        Wait until a request can be made, if necessary.
        
        This method will block until a token is available.
        
        Returns:
            The time waited in seconds
        """
        start_time = time.time()
        
        with self.lock:
            self._refill_tokens()
            
            if self.tokens >= 1:
                # Token is available, no need to wait
                self.tokens -= 1
                return 0.0
            
            # Calculate how long to wait for the next token
            # Time until one token becomes available
            time_until_token = self.time_window / self.max_requests
        
        # Wait outside the lock to allow other threads to check
        time.sleep(time_until_token)
        
        # After waiting, consume a token
        with self.lock:
            self._refill_tokens()
            if self.tokens >= 1:
                self.tokens -= 1
        
        wait_time = time.time() - start_time
        logger.debug(f"Waited {wait_time:.2f} seconds for rate limit")
        return wait_time
    
    def acquire_token(self) -> bool:
        """
        Try to acquire a token for making a request.
        
        Returns:
            True if a token was acquired, False if no tokens are available
        """
        with self.lock:
            self._refill_tokens()
            
            if self.tokens >= 1:
                self.tokens -= 1
                logger.debug("Token acquired for request")
                return True
            
            logger.debug("No tokens available for request")
            return False
    
    def get_available_tokens(self) -> int:
        """
        Get the current number of available tokens.
        
        Returns:
            The number of available tokens (integer)
        """
        with self.lock:
            self._refill_tokens()
            return int(self.tokens)
    
    def get_time_until_next_token(self) -> float:
        """
        Get the time in seconds until the next token becomes available.
        
        Returns:
            Time in seconds until next token, or 0 if tokens are available now
        """
        with self.lock:
            self._refill_tokens()
            
            if self.tokens >= 1:
                return 0.0
            
            # Calculate time until one token becomes available
            return self.time_window / self.max_requests
    
    def reset(self) -> None:
        """
        Reset the rate limiter to its initial state.
        
        This method refills the token bucket to maximum capacity.
        """
        with self.lock:
            self.tokens = self.max_requests
            self.last_refill = time.time()
            logger.debug("RateLimiter reset to initial state")