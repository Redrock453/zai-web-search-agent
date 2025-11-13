# Batch search example for the Z.AI Web Search Agent
# This file demonstrates how to perform multiple searches efficiently

import os
import sys
import time
import json
import csv
from typing import List, Dict, Any, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

# Add the parent directory to the path so we can import the agent module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import (
    WebSearchAgent, 
    ZAIConfig, 
    ZAIAuthenticator,
    SearchRequest,
    ZAIAuthenticationError,
    ZAIRateLimitError,
    ZAIInvalidRequestError,
    ZAIApiError
)


@dataclass
class BatchSearchItem:
    """
    Represents a single item in a batch search
    """
    id: str
    query: str
    search_type: str = "web"
    num_results: int = 10
    language: Optional[str] = None
    region: Optional[str] = None
    include_domains: Optional[List[str]] = None
    exclude_domains: Optional[List[str]] = None
    safe_search: str = "moderate"


@dataclass
class BatchSearchResult:
    """
    Represents the result of a batch search operation
    """
    item: BatchSearchItem
    results: Any  # SearchResponse
    execution_time: float
    success: bool
    error_message: Optional[str] = None


class BatchSearchProcessor:
    """
    Handles batch search operations with multiple queries
    """
    
    def __init__(self, agent: WebSearchAgent, max_workers: int = 5):
        """
        Initialize the batch search processor
        
        Args:
            agent: WebSearchAgent instance
            max_workers: Maximum number of concurrent workers
        """
        self.agent = agent
        self.max_workers = max_workers
    
    def process_batch(self, items: List[BatchSearchItem]) -> List[BatchSearchResult]:
        """
        Process a batch of search items
        
        Args:
            items: List of BatchSearchItem objects
            
        Returns:
            List of BatchSearchResult objects
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_item = {
                executor.submit(self._process_single_item, item): item 
                for item in items
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(BatchSearchResult(
                        item=item,
                        results=None,
                        execution_time=0.0,
                        success=False,
                        error_message=str(e)
                    ))
        
        # Sort results by item ID to maintain order
        results.sort(key=lambda x: x.item.id)
        return results
    
    def _process_single_item(self, item: BatchSearchItem) -> BatchSearchResult:
        """
        Process a single search item
        
        Args:
            item: BatchSearchItem to process
            
        Returns:
            BatchSearchResult with the search results
        """
        start_time = time.time()
        
        try:
            # Create search request
            request = SearchRequest(
                query=item.query,
                num_results=item.num_results,
                search_type=item.search_type,
                language=item.language,
                region=item.region,
                include_domains=item.include_domains,
                exclude_domains=item.exclude_domains,
                safe_search=item.safe_search
            )
            
            # Execute search
            results = self.agent.search_with_request(request)
            
            execution_time = time.time() - start_time
            
            return BatchSearchResult(
                item=item,
                results=results,
                execution_time=execution_time,
                success=True
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            return BatchSearchResult(
                item=item,
                results=None,
                execution_time=execution_time,
                success=False,
                error_message=str(e)
            )
    
    def process_batch_sequential(self, items: List[BatchSearchItem]) -> List[BatchSearchResult]:
        """
        Process a batch of search items sequentially (one at a time)
        
        Args:
            items: List of BatchSearchItem objects
            
        Returns:
            List of BatchSearchResult objects
        """
        results = []
        
        for item in items:
            result = self._process_single_item(item)
            results.append(result)
        
        return results


def basic_batch_search_example():
    """
    Example of a basic batch search
    """
    print("=== Basic Batch Search Example ===")
    
    try:
        # Initialize the agent
        agent = WebSearchAgent()
        processor = BatchSearchProcessor(agent, max_workers=3)
        
        # Define search items
        items = [
            BatchSearchItem(id="1", query="artificial intelligence trends"),
            BatchSearchItem(id="2", query="machine learning applications"),
            BatchSearchItem(id="3", query="deep learning frameworks"),
            BatchSearchItem(id="4", query="natural language processing"),
            BatchSearchItem(id="5", query="computer vision applications")
        ]
        
        # Process batch
        start_time = time.time()
        results = processor.process_batch(items)
        end_time = time.time()
        
        # Display results
        print(f"Processed {len(items)} searches in {end_time - start_time:.2f} seconds")
        
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        
        print(f"Successful searches: {successful}")
        print(f"Failed searches: {failed}")
        
        for result in results:
            if result.success:
                print(f"\nID {result.item.id}: '{result.item.query}'")
                print(f"  Results: {len(result.results.results)} items")
                print(f"  Execution time: {result.execution_time:.2f} seconds")
                print(f"  Top result: {result.results.results[0].title}")
            else:
                print(f"\nID {result.item.id}: '{result.item.query}' - FAILED")
                print(f"  Error: {result.error_message}")
        
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


def advanced_batch_search_example():
    """
    Example of an advanced batch search with different search types
    """
    print("\n=== Advanced Batch Search Example ===")
    
    try:
        # Initialize the agent
        agent = WebSearchAgent()
        processor = BatchSearchProcessor(agent, max_workers=5)
        
        # Define search items with different types and parameters
        items = [
            BatchSearchItem(
                id="web1",
                query="latest AI research",
                search_type="web",
                num_results=10,
                language="en",
                safe_search="moderate"
            ),
            BatchSearchItem(
                id="news1",
                query="artificial intelligence breakthrough",
                search_type="news",
                num_results=8,
                language="en",
                include_domains=["techcrunch.com", "wired.com", "arstechnica.com"]
            ),
            BatchSearchItem(
                id="web2",
                query="machine learning healthcare",
                search_type="web",
                num_results=5,
                language="en",
                include_domains=["nature.com", "science.org", "nejm.org"]
            ),
            BatchSearchItem(
                id="images1",
                query="AI generated art",
                search_type="images",
                num_results=5,
                safe_search="moderate"
            ),
            BatchSearchItem(
                id="web3",
                query="quantum computing applications",
                search_type="web",
                num_results=7,
                language="en",
                exclude_domains=["spam.com", "fake-news.com"]
            )
        ]
        
        # Process batch
        start_time = time.time()
        results = processor.process_batch(items)
        end_time = time.time()
        
        # Display results
        print(f"Processed {len(items)} advanced searches in {end_time - start_time:.2f} seconds")
        
        for result in results:
            if result.success:
                print(f"\nID {result.item.id}: '{result.item.query}' ({result.item.search_type})")
                print(f"  Results: {len(result.results.results)} items")
                print(f"  Execution time: {result.execution_time:.2f} seconds")
                print(f"  Search time: {result.results.search_time:.2f} seconds")
                print(f"  Total available: {result.results.total_results}")
                if result.results.results:
                    print(f"  Top result: {result.results.results[0].title}")
            else:
                print(f"\nID {result.item.id}: '{result.item.query}' - FAILED")
                print(f"  Error: {result.error_message}")
        
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


def sequential_vs_concurrent_batch_example():
    """
    Example comparing sequential vs concurrent batch search performance
    """
    print("\n=== Sequential vs Concurrent Batch Search Example ===")
    
    try:
        # Initialize the agent
        agent = WebSearchAgent()
        processor = BatchSearchProcessor(agent, max_workers=5)
        
        # Define search items
        items = [
            BatchSearchItem(id=f"search_{i}", query=f"artificial intelligence research paper {i+1}")
            for i in range(8)
        ]
        
        # Sequential processing
        print("Running batch search sequentially...")
        sequential_start = time.time()
        sequential_results = processor.process_batch_sequential(items)
        sequential_end = time.time()
        sequential_time = sequential_end - sequential_start
        
        # Concurrent processing
        print("Running batch search concurrently...")
        concurrent_start = time.time()
        concurrent_results = processor.process_batch(items)
        concurrent_end = time.time()
        concurrent_time = concurrent_end - concurrent_start
        
        # Compare results
        print(f"\nPerformance comparison:")
        print(f"Sequential processing time: {sequential_time:.2f} seconds")
        print(f"Concurrent processing time: {concurrent_time:.2f} seconds")
        print(f"Performance improvement: {sequential_time/concurrent_time:.2f}x faster")
        
        # Verify results are the same
        sequential_successful = sum(1 for r in sequential_results if r.success)
        concurrent_successful = sum(1 for r in concurrent_results if r.success)
        
        print(f"Sequential successful searches: {sequential_successful}/{len(items)}")
        print(f"Concurrent successful searches: {concurrent_successful}/{len(items)}")
        
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


def export_batch_results_example():
    """
    Example of exporting batch search results to different formats
    """
    print("\n=== Export Batch Results Example ===")
    
    try:
        # Initialize the agent
        agent = WebSearchAgent()
        processor = BatchSearchProcessor(agent, max_workers=3)
        
        # Define search items
        items = [
            BatchSearchItem(id="ai1", query="artificial intelligence ethics"),
            BatchSearchItem(id="ml1", query="machine learning algorithms"),
            BatchSearchItem(id="dl1", query="deep learning architectures"),
            BatchSearchItem(id="nlp1", query="natural language processing models")
        ]
        
        # Process batch
        results = processor.process_batch(items)
        
        # Export to JSON
        export_to_json(results, "batch_search_results.json")
        print("Results exported to batch_search_results.json")
        
        # Export to CSV
        export_to_csv(results, "batch_search_results.csv")
        print("Results exported to batch_search_results.csv")
        
        # Export summary to text
        export_summary_to_text(results, "batch_search_summary.txt")
        print("Summary exported to batch_search_summary.txt")
        
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


def export_to_json(results: List[BatchSearchResult], filename: str):
    """
    Export batch search results to JSON format
    
    Args:
        results: List of BatchSearchResult objects
        filename: Output filename
    """
    export_data = []
    
    for result in results:
        item_data = {
            "id": result.item.id,
            "query": result.item.query,
            "search_type": result.item.search_type,
            "success": result.success,
            "execution_time": result.execution_time,
            "error_message": result.error_message
        }
        
        if result.success:
            item_data["total_results"] = result.results.total_results
            item_data["search_time"] = result.results.search_time
            item_data["results_count"] = len(result.results.results)
            
            # Add top 3 results
            item_data["top_results"] = []
            for search_result in result.results.results[:3]:
                item_data["top_results"].append({
                    "title": search_result.title,
                    "url": search_result.url,
                    "snippet": search_result.snippet[:100] + "..." if len(search_result.snippet) > 100 else search_result.snippet,
                    "domain": search_result.domain
                })
        
        export_data.append(item_data)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)


def export_to_csv(results: List[BatchSearchResult], filename: str):
    """
    Export batch search results to CSV format
    
    Args:
        results: List of BatchSearchResult objects
        filename: Output filename
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            "ID", "Query", "Search Type", "Success", "Execution Time",
            "Total Results", "Search Time", "Top Result Title", "Top Result URL"
        ])
        
        # Write data
        for result in results:
            row = [
                result.item.id,
                result.item.query,
                result.item.search_type,
                result.success,
                result.execution_time
            ]
            
            if result.success and result.results.results:
                row.extend([
                    result.results.total_results,
                    result.results.search_time,
                    result.results.results[0].title,
                    result.results.results[0].url
                ])
            else:
                row.extend(["", "", "", ""])
            
            writer.writerow(row)


def export_summary_to_text(results: List[BatchSearchResult], filename: str):
    """
    Export a summary of batch search results to text format
    
    Args:
        results: List of BatchSearchResult objects
        filename: Output filename
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Batch Search Results Summary\n")
        f.write("=" * 40 + "\n\n")
        
        # Overall statistics
        total = len(results)
        successful = sum(1 for r in results if r.success)
        failed = total - successful
        total_execution_time = sum(r.execution_time for r in results)
        
        f.write(f"Total searches: {total}\n")
        f.write(f"Successful: {successful}\n")
        f.write(f"Failed: {failed}\n")
        f.write(f"Success rate: {successful/total*100:.1f}%\n")
        f.write(f"Total execution time: {total_execution_time:.2f} seconds\n")
        f.write(f"Average execution time: {total_execution_time/total:.2f} seconds\n\n")
        
        # Individual results
        f.write("Individual Results:\n")
        f.write("-" * 20 + "\n")
        
        for result in results:
            f.write(f"\nID: {result.item.id}\n")
            f.write(f"Query: {result.item.query}\n")
            f.write(f"Type: {result.item.search_type}\n")
            f.write(f"Success: {result.success}\n")
            f.write(f"Execution time: {result.execution_time:.2f} seconds\n")
            
            if result.success:
                f.write(f"Total results: {result.results.total_results}\n")
                f.write(f"Search time: {result.results.search_time:.2f} seconds\n")
                if result.results.results:
                    f.write(f"Top result: {result.results.results[0].title}\n")
            else:
                f.write(f"Error: {result.error_message}\n")


def error_handling_batch_example():
    """
    Example of error handling in batch search operations
    """
    print("\n=== Batch Search Error Handling Example ===")
    
    try:
        # Initialize the agent
        agent = WebSearchAgent()
        processor = BatchSearchProcessor(agent, max_workers=3)
        
        # Define search items with some that will fail
        items = [
            BatchSearchItem(id="valid1", query="artificial intelligence"),
            BatchSearchItem(id="invalid1", query="test", search_type="invalid_type"),  # Will fail
            BatchSearchItem(id="valid2", query="machine learning"),
            BatchSearchItem(id="invalid2", query="test", num_results=25),  # Will fail (too many results)
            BatchSearchItem(id="valid3", query="deep learning")
        ]
        
        # Process batch
        results = processor.process_batch(items)
        
        # Display results
        print(f"Processed {len(items)} searches with mixed success/failure:")
        
        successful = 0
        failed = 0
        
        for result in results:
            if result.success:
                successful += 1
                print(f"  ✓ ID {result.item.id}: '{result.item.query}' - {len(result.results.results)} results")
            else:
                failed += 1
                print(f"  ✗ ID {result.item.id}: '{result.item.query}' - {result.error_message}")
        
        print(f"\nSummary: {successful} successful, {failed} failed")
        
        # Retry failed searches with corrected parameters
        if failed > 0:
            print("\nRetrying failed searches with corrected parameters...")
            
            retry_items = []
            for result in results:
                if not result.success:
                    item = result.item
                    
                    # Fix the issues
                    if item.search_type == "invalid_type":
                        item.search_type = "web"
                    if item.num_results > 20:
                        item.num_results = 10
                    
                    retry_items.append(item)
            
            # Retry the failed searches
            retry_results = processor.process_batch(retry_items)
            
            for result in retry_results:
                if result.success:
                    print(f"  ✓ Retry ID {result.item.id}: '{result.item.query}' - {len(result.results.results)} results")
                else:
                    print(f"  ✗ Retry ID {result.item.id}: '{result.item.query}' - {result.error_message}")
        
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


def main():
    """
    Run all batch search examples
    """
    print("Z.AI Web Search Agent - Batch Search Examples")
    print("=" * 50)
    
    # Run all examples
    basic_batch_search_example()
    advanced_batch_search_example()
    sequential_vs_concurrent_batch_example()
    export_batch_results_example()
    error_handling_batch_example()
    
    print("\n" + "=" * 50)
    print("Batch search examples completed!")
    print("\nNote: Some examples may fail if you don't have a valid API key configured.")
    print("Please set your ZAI_API_KEY in the .env file or in your environment variables.")
    print("\nGenerated files:")
    print("- batch_search_results.json")
    print("- batch_search_results.csv")
    print("- batch_search_summary.txt")


if __name__ == "__main__":
    main()