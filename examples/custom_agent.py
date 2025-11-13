# Custom agent example for the Z.AI Web Search Agent
# This file demonstrates how to extend the base WebSearchAgent with additional functionality

import os
import sys
import time
import json
import re
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime

# Add the parent directory to the path so we can import the agent module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import (
    WebSearchAgent, 
    ZAIConfig, 
    ZAIAuthenticator,
    SearchRequest,
    SearchResult,
    SearchResponse,
    ZAIAuthenticationError,
    ZAIRateLimitError,
    ZAIInvalidRequestError,
    ZAIApiError
)


@dataclass
class EnhancedSearchResult:
    """
    Enhanced search result with additional metadata
    """
    # Original SearchResult fields
    title: str
    url: str
    snippet: str
    position: int
    domain: str
    published_date: Optional[str] = None
    thumbnail_url: Optional[str] = None
    
    # Enhanced fields
    word_count: int = 0
    reading_time_minutes: float = 0.0
    sentiment_score: float = 0.0  # -1 to 1, negative to positive
    key_phrases: List[str] = None
    content_type: str = "unknown"  # article, blog, news, etc.
    credibility_score: float = 0.0  # 0 to 1, low to high credibility
    
    def __post_init__(self):
        """Initialize derived fields"""
        if self.key_phrases is None:
            self.key_phrases = []


@dataclass
class SearchSummary:
    """
    Summary of search results with analytics
    """
    query: str
    total_results: int
    results_count: int
    search_time: float
    execution_time: float
    
    # Analytics
    average_word_count: float = 0.0
    average_reading_time: float = 0.0
    sentiment_distribution: Dict[str, int] = None
    domain_distribution: Dict[str, int] = None
    content_type_distribution: Dict[str, int] = None
    top_domains: List[Tuple[str, int]] = None
    key_topics: List[str] = None
    
    def __post_init__(self):
        """Initialize derived fields"""
        if self.sentiment_distribution is None:
            self.sentiment_distribution = {"positive": 0, "neutral": 0, "negative": 0}
        if self.domain_distribution is None:
            self.domain_distribution = {}
        if self.content_type_distribution is None:
            self.content_type_distribution = {}
        if self.top_domains is None:
            self.top_domains = []
        if self.key_topics is None:
            self.key_topics = []


class CustomWebSearchAgent(WebSearchAgent):
    """
    Custom web search agent with enhanced functionality
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the custom web search agent
        
        Args:
            *args: Positional arguments to pass to WebSearchAgent
            **kwargs: Keyword arguments to pass to WebSearchAgent
        """
        super().__init__(*args, **kwargs)
        
        # Custom configuration
        self.enable_result_enhancement = True
        self.enable_analytics = True
        self.reading_speed_wpm = 200  # Average reading speed
        
        # Domain credibility scores (0-1, higher is more credible)
        self.domain_credibility = {
            "nature.com": 0.95,
            "science.org": 0.95,
            "nejm.org": 0.95,
            "thelancet.com": 0.95,
            "arxiv.org": 0.90,
            "pubmed.ncbi.nlm.nih.gov": 0.90,
            "mit.edu": 0.90,
            "stanford.edu": 0.90,
            "harvard.edu": 0.90,
            "bbc.com": 0.85,
            "reuters.com": 0.85,
            "apnews.com": 0.85,
            "npr.org": 0.80,
            "wired.com": 0.75,
            "techcrunch.com": 0.75,
            "medium.com": 0.60,
            "blogspot.com": 0.40,
            "wordpress.com": 0.40
        }
    
    def search_with_enhancement(
        self,
        query: str,
        num_results: int = 10,
        include_domains: Optional[list] = None,
        exclude_domains: Optional[list] = None,
        search_type: str = "web",
        language: Optional[str] = None,
        region: Optional[str] = None,
        safe_search: str = "moderate"
    ) -> Tuple[List[EnhancedSearchResult], SearchSummary]:
        """
        Perform a search with enhanced results and analytics
        
        Args:
            query: Search query string
            num_results: Number of results to return
            include_domains: List of domains to include
            exclude_domains: List of domains to exclude
            search_type: Type of search
            language: Language code
            region: Region code
            safe_search: Safe search level
            
        Returns:
            Tuple of (enhanced results, search summary)
        """
        start_time = time.time()
        
        # Perform the base search
        response = self.search(
            query=query,
            num_results=num_results,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            search_type=search_type,
            language=language,
            region=region,
            safe_search=safe_search
        )
        
        execution_time = time.time() - start_time
        
        # Enhance results if enabled
        if self.enable_result_enhancement:
            enhanced_results = self._enhance_results(response.results)
        else:
            # Convert to EnhancedSearchResult without enhancement
            enhanced_results = [
                EnhancedSearchResult(
                    title=result.title,
                    url=result.url,
                    snippet=result.snippet,
                    position=result.position,
                    domain=result.domain,
                    published_date=result.published_date,
                    thumbnail_url=result.thumbnail_url
                )
                for result in response.results
            ]
        
        # Generate analytics if enabled
        if self.enable_analytics:
            summary = self._generate_summary(response, enhanced_results, execution_time)
        else:
            summary = SearchSummary(
                query=response.query,
                total_results=response.total_results,
                results_count=len(response.results),
                search_time=response.search_time,
                execution_time=execution_time
            )
        
        return enhanced_results, summary
    
    def _enhance_results(self, results: List[SearchResult]) -> List[EnhancedSearchResult]:
        """
        Enhance search results with additional metadata
        
        Args:
            results: Original search results
            
        Returns:
            List of enhanced search results
        """
        enhanced_results = []
        
        for result in results:
            # Estimate word count from snippet (rough approximation)
            word_count = len(result.snippet.split())
            
            # Estimate reading time
            reading_time = word_count / self.reading_speed_wpm
            
            # Simple sentiment analysis based on keywords
            sentiment_score = self._analyze_sentiment(result.snippet)
            
            # Extract key phrases
            key_phrases = self._extract_key_phrases(result.snippet)
            
            # Determine content type
            content_type = self._determine_content_type(result.url, result.title)
            
            # Get credibility score
            credibility_score = self._get_credibility_score(result.domain)
            
            # Create enhanced result
            enhanced_result = EnhancedSearchResult(
                title=result.title,
                url=result.url,
                snippet=result.snippet,
                position=result.position,
                domain=result.domain,
                published_date=result.published_date,
                thumbnail_url=result.thumbnail_url,
                word_count=word_count,
                reading_time_minutes=reading_time,
                sentiment_score=sentiment_score,
                key_phrases=key_phrases,
                content_type=content_type,
                credibility_score=credibility_score
            )
            
            enhanced_results.append(enhanced_result)
        
        return enhanced_results
    
    def _analyze_sentiment(self, text: str) -> float:
        """
        Simple sentiment analysis based on keyword matching
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment score from -1 (negative) to 1 (positive)
        """
        # Simple keyword-based sentiment analysis
        positive_words = [
            "good", "great", "excellent", "amazing", "wonderful", "fantastic",
            "positive", "success", "benefit", "advantage", "improvement", "breakthrough"
        ]
        
        negative_words = [
            "bad", "terrible", "awful", "horrible", "negative", "failure",
            "problem", "issue", "disadvantage", "decline", "risk", "threat"
        ]
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        # Count positive and negative words
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Calculate sentiment score
        total_words = positive_count + negative_count
        if total_words == 0:
            return 0.0  # Neutral
        
        return (positive_count - negative_count) / total_words
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """
        Extract key phrases from text
        
        Args:
            text: Text to extract phrases from
            
        Returns:
            List of key phrases
        """
        # Simple key phrase extraction based on common patterns
        # This is a basic implementation - in practice, you might use NLP libraries
        
        # Remove common stop words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "is", "are", "was", "were", "be", "been", "have",
            "has", "had", "do", "does", "did", "will", "would", "could", "should"
        }
        
        # Split into words and filter stop words
        words = re.findall(r'\b\w+\b', text.lower())
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequency
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top words as key phrases
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        key_phrases = [word for word, freq in top_words[:5]]
        
        return key_phrases
    
    def _determine_content_type(self, url: str, title: str) -> str:
        """
        Determine the content type based on URL and title
        
        Args:
            url: URL of the content
            title: Title of the content
            
        Returns:
            Content type string
        """
        url_lower = url.lower()
        title_lower = title.lower()
        
        # Check for common content type indicators
        if any(indicator in url_lower for indicator in ["blog", "post", "article"]):
            return "blog"
        elif any(indicator in url_lower for indicator in ["news", "press", "release"]):
            return "news"
        elif any(indicator in url_lower for indicator in ["research", "paper", "study", "journal"]):
            return "research"
        elif any(indicator in url_lower for indicator in ["product", "service", "solution"]):
            return "commercial"
        elif any(indicator in url_lower for indicator in ["wiki", "documentation", "docs"]):
            return "documentation"
        elif any(indicator in title_lower for indicator in ["how to", "tutorial", "guide"]):
            return "tutorial"
        elif any(indicator in title_lower for indicator in ["review", "analysis", "opinion"]):
            return "review"
        else:
            return "article"
    
    def _get_credibility_score(self, domain: str) -> float:
        """
        Get credibility score for a domain
        
        Args:
            domain: Domain name
            
        Returns:
            Credibility score from 0 (low) to 1 (high)
        """
        # Check if domain is in our credibility database
        if domain in self.domain_credibility:
            return self.domain_credibility[domain]
        
        # For unknown domains, use heuristics
        domain_lower = domain.lower()
        
        # Educational domains tend to be more credible
        if domain_lower.endswith(".edu") or domain_lower.endswith(".ac."):
            return 0.85
        
        # Government domains
        if domain_lower.endswith(".gov") or domain_lower.endswith(".gov."):
            return 0.90
        
        # Organization domains
        if domain_lower.endswith(".org"):
            return 0.70
        
        # Commercial domains
        if domain_lower.endswith(".com"):
            return 0.60
        
        # Default credibility for unknown domains
        return 0.50
    
    def _generate_summary(
        self,
        response: SearchResponse,
        enhanced_results: List[EnhancedSearchResult],
        execution_time: float
    ) -> SearchSummary:
        """
        Generate a summary with analytics
        
        Args:
            response: Original search response
            enhanced_results: Enhanced search results
            execution_time: Total execution time
            
        Returns:
            Search summary with analytics
        """
        summary = SearchSummary(
            query=response.query,
            total_results=response.total_results,
            results_count=len(response.results),
            search_time=response.search_time,
            execution_time=execution_time
        )
        
        if not enhanced_results:
            return summary
        
        # Calculate averages
        summary.average_word_count = sum(r.word_count for r in enhanced_results) / len(enhanced_results)
        summary.average_reading_time = sum(r.reading_time_minutes for r in enhanced_results) / len(enhanced_results)
        
        # Sentiment distribution
        for result in enhanced_results:
            if result.sentiment_score > 0.1:
                summary.sentiment_distribution["positive"] += 1
            elif result.sentiment_score < -0.1:
                summary.sentiment_distribution["negative"] += 1
            else:
                summary.sentiment_distribution["neutral"] += 1
        
        # Domain distribution
        for result in enhanced_results:
            summary.domain_distribution[result.domain] = summary.domain_distribution.get(result.domain, 0) + 1
        
        # Content type distribution
        for result in enhanced_results:
            summary.content_type_distribution[result.content_type] = summary.content_type_distribution.get(result.content_type, 0) + 1
        
        # Top domains
        summary.top_domains = sorted(
            summary.domain_distribution.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Extract key topics from all results
        all_key_phrases = []
        for result in enhanced_results:
            all_key_phrases.extend(result.key_phrases)
        
        # Count frequency of key phrases
        key_phrase_freq = {}
        for phrase in all_key_phrases:
            key_phrase_freq[phrase] = key_phrase_freq.get(phrase, 0) + 1
        
        # Get top key phrases as topics
        summary.key_topics = [
            phrase for phrase, freq in sorted(key_phrase_freq.items(), key=lambda x: x[1], reverse=True)
        ][:10]
        
        return summary
    
    def search_by_sentiment(
        self,
        query: str,
        sentiment: str = "positive",
        num_results: int = 10
    ) -> List[EnhancedSearchResult]:
        """
        Search and filter results by sentiment
        
        Args:
            query: Search query
            sentiment: Desired sentiment ("positive", "negative", "neutral")
            num_results: Number of results to return
            
        Returns:
            List of enhanced search results filtered by sentiment
        """
        # Perform enhanced search
        enhanced_results, _ = self.search_with_enhancement(query, num_results * 2)  # Get more to filter
        
        # Filter by sentiment
        if sentiment == "positive":
            filtered = [r for r in enhanced_results if r.sentiment_score > 0.1]
        elif sentiment == "negative":
            filtered = [r for r in enhanced_results if r.sentiment_score < -0.1]
        elif sentiment == "neutral":
            filtered = [r for r in enhanced_results if -0.1 <= r.sentiment_score <= 0.1]
        else:
            filtered = enhanced_results
        
        # Return requested number of results
        return filtered[:num_results]
    
    def search_by_credibility(
        self,
        query: str,
        min_credibility: float = 0.7,
        num_results: int = 10
    ) -> List[EnhancedSearchResult]:
        """
        Search and filter results by credibility score
        
        Args:
            query: Search query
            min_credibility: Minimum credibility score (0-1)
            num_results: Number of results to return
            
        Returns:
            List of enhanced search results filtered by credibility
        """
        # Perform enhanced search
        enhanced_results, _ = self.search_with_enhancement(query, num_results * 2)  # Get more to filter
        
        # Filter by credibility
        filtered = [r for r in enhanced_results if r.credibility_score >= min_credibility]
        
        # Sort by credibility (highest first)
        filtered.sort(key=lambda x: x.credibility_score, reverse=True)
        
        # Return requested number of results
        return filtered[:num_results]
    
    def compare_queries(
        self,
        queries: List[str],
        num_results: int = 10
    ) -> Dict[str, Tuple[List[EnhancedSearchResult], SearchSummary]]:
        """
        Compare search results for multiple queries
        
        Args:
            queries: List of search queries
            num_results: Number of results per query
            
        Returns:
            Dictionary mapping query to (results, summary)
        """
        comparison = {}
        
        for query in queries:
            enhanced_results, summary = self.search_with_enhancement(query, num_results)
            comparison[query] = (enhanced_results, summary)
        
        return comparison


def basic_custom_agent_example():
    """
    Example of using the custom web search agent
    """
    print("=== Basic Custom Agent Example ===")
    
    try:
        # Initialize the custom agent
        agent = CustomWebSearchAgent()
        
        # Perform an enhanced search
        query = "artificial intelligence in healthcare"
        enhanced_results, summary = agent.search_with_enhancement(query, num_results=5)
        
        # Display summary
        print(f"Search summary for '{query}':")
        print(f"  Total results available: {summary.total_results}")
        print(f"  Results returned: {summary.results_count}")
        print(f"  Search time: {summary.search_time:.2f} seconds")
        print(f"  Execution time: {summary.execution_time:.2f} seconds")
        print(f"  Average word count: {summary.average_word_count:.0f}")
        print(f"  Average reading time: {summary.average_reading_time:.1f} minutes")
        
        # Display sentiment distribution
        print(f"\nSentiment distribution:")
        for sentiment, count in summary.sentiment_distribution.items():
            print(f"  {sentiment}: {count}")
        
        # Display top domains
        print(f"\nTop domains:")
        for domain, count in summary.top_domains:
            print(f"  {domain}: {count}")
        
        # Display enhanced results
        print(f"\nEnhanced results:")
        for result in enhanced_results[:3]:
            print(f"\n  {result.title}")
            print(f"    URL: {result.url}")
            print(f"    Content type: {result.content_type}")
            print(f"    Credibility score: {result.credibility_score:.2f}")
            print(f"    Sentiment score: {result.sentiment_score:.2f}")
            print(f"    Reading time: {result.reading_time_minutes:.1f} minutes")
            print(f"    Key phrases: {', '.join(result.key_phrases[:3])}")
            print(f"    Snippet: {result.snippet[:100]}...")
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
        print("Please check your API key in the .env file")
    except ZAIRateLimitError as e:
        print(f"Rate limit error: {e.message}")
        print("Please wait before making more requests")
    except ZAIInvalidRequestError as e:
        print(f"Invalid request error: {e.message}")
        print("Please check your search parameters")
    except ZAIApiError as e:
        print(f"API error: {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def sentiment_search_example():
    """
    Example of searching by sentiment
    """
    print("\n=== Sentiment-based Search Example ===")
    
    try:
        # Initialize the custom agent
        agent = CustomWebSearchAgent()
        
        query = "climate change"
        
        # Search for positive sentiment results
        print(f"Searching for positive sentiment results for '{query}':")
        positive_results = agent.search_by_sentiment(query, sentiment="positive", num_results=3)
        
        for result in positive_results:
            print(f"\n  {result.title}")
            print(f"    Sentiment score: {result.sentiment_score:.2f}")
            print(f"    Snippet: {result.snippet[:100]}...")
        
        # Search for negative sentiment results
        print(f"\nSearching for negative sentiment results for '{query}':")
        negative_results = agent.search_by_sentiment(query, sentiment="negative", num_results=3)
        
        for result in negative_results:
            print(f"\n  {result.title}")
            print(f"    Sentiment score: {result.sentiment_score:.2f}")
            print(f"    Snippet: {result.snippet[:100]}...")
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
    except ZAIRateLimitError as e:
        print(f"Rate limit error: {e.message}")
    except ZAIInvalidRequestError as e:
        print(f"Invalid request error: {e.message}")
    except ZAIApiError as e:
        print(f"API error: {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def credibility_search_example():
    """
    Example of searching by credibility
    """
    print("\n=== Credibility-based Search Example ===")
    
    try:
        # Initialize the custom agent
        agent = CustomWebSearchAgent()
        
        query = "medical research"
        
        # Search for high credibility results
        print(f"Searching for high credibility results for '{query}':")
        credible_results = agent.search_by_credibility(query, min_credibility=0.8, num_results=5)
        
        for result in credible_results:
            print(f"\n  {result.title}")
            print(f"    Domain: {result.domain}")
            print(f"    Credibility score: {result.credibility_score:.2f}")
            print(f"    Content type: {result.content_type}")
            print(f"    Snippet: {result.snippet[:100]}...")
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
    except ZAIRateLimitError as e:
        print(f"Rate limit error: {e.message}")
    except ZAIInvalidRequestError as e:
        print(f"Invalid request error: {e.message}")
    except ZAIApiError as e:
        print(f"API error: {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def query_comparison_example():
    """
    Example of comparing multiple queries
    """
    print("\n=== Query Comparison Example ===")
    
    try:
        # Initialize the custom agent
        agent = CustomWebSearchAgent()
        
        # Define queries to compare
        queries = [
            "artificial intelligence",
            "machine learning",
            "deep learning"
        ]
        
        # Compare queries
        comparison = agent.compare_queries(queries, num_results=5)
        
        # Display comparison
        for query, (results, summary) in comparison.items():
            print(f"\nQuery: '{query}'")
            print(f"  Results: {summary.results_count}")
            print(f"  Average reading time: {summary.average_reading_time:.1f} minutes")
            print(f"  Top domains: {', '.join([domain for domain, _ in summary.top_domains[:3]])}")
            print(f"  Key topics: {', '.join(summary.key_topics[:5])}")
            
            # Show sentiment distribution
            total = sum(summary.sentiment_distribution.values())
            if total > 0:
                positive_pct = summary.sentiment_distribution["positive"] / total * 100
                print(f"  Positive sentiment: {positive_pct:.0f}%")
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
    except ZAIRateLimitError as e:
        print(f"Rate limit error: {e.message}")
    except ZAIInvalidRequestError as e:
        print(f"Invalid request error: {e.message}")
    except ZAIApiError as e:
        print(f"API error: {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def custom_configuration_example():
    """
    Example of using custom configuration with the custom agent
    """
    print("\n=== Custom Configuration Example ===")
    
    try:
        # Create custom configuration
        config = ZAIConfig.from_env()
        
        # Initialize the custom agent with custom settings
        agent = CustomWebSearchAgent(
            config=config,
            max_retries=5,
            initial_backoff=1.5,
            max_backoff=30.0,
            rate_limit_requests=50,
            rate_limit_window=60
        )
        
        # Customize agent settings
        agent.enable_result_enhancement = True
        agent.enable_analytics = True
        agent.reading_speed_wpm = 250  # Faster reading speed
        
        # Add custom domain credibility scores
        agent.domain_credibility.update({
            "custom-domain.com": 0.95,
            "another-domain.org": 0.80
        })
        
        # Perform search with custom configuration
        query = "quantum computing"
        enhanced_results, summary = agent.search_with_enhancement(query, num_results=3)
        
        # Display results
        print(f"Custom search for '{query}':")
        print(f"  Custom reading speed: {agent.reading_speed_wpm} WPM")
        print(f"  Results: {summary.results_count}")
        
        for result in enhanced_results:
            print(f"\n  {result.title}")
            print(f"    Credibility score: {result.credibility_score:.2f}")
            print(f"    Reading time: {result.reading_time_minutes:.1f} minutes")
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
        print("Please check your API key in the .env file")
    except ZAIRateLimitError as e:
        print(f"Rate limit error: {e.message}")
    except ZAIInvalidRequestError as e:
        print(f"Invalid request error: {e.message}")
    except ZAIApiError as e:
        print(f"API error: {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    """
    Run all custom agent examples
    """
    print("Z.AI Web Search Agent - Custom Agent Examples")
    print("=" * 50)
    
    # Run all examples
    basic_custom_agent_example()
    sentiment_search_example()
    credibility_search_example()
    query_comparison_example()
    custom_configuration_example()
    
    print("\n" + "=" * 50)
    print("Custom agent examples completed!")
    print("\nNote: Some examples may fail if you don't have a valid API key configured.")
    print("Please set your ZAI_API_KEY in the .env file or in your environment variables.")


if __name__ == "__main__":
    main()