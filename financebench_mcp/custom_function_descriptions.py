# Define custom tool descriptions
CUSTOM_TOOL_DESCRIPTIONS = """
search_file_contents:
Description: Searches through a large document and retrieves the most relevant text chunks based on a query
Arguments:
  document_name (required) - Path to the document file to search (PDF or text)
  query (required) - The search query to find relevant information in the document
  retrieval_method (optional) - Method to use for retrieval: "bm25" (keyword-based) or "embedding" (semantic)
  keywords (optional) - List of specific keywords to search for (MUST BE USED WITH BM25 METHOD)
  top_k (optional) - Number of text chunks to return (higher values return more content)
  chunk_size (optional) - Size of each text chunk in characters (affects context window size)

visualize_financial_data:
Description: Creates visualizations for financial data extracted from documents
Arguments:
  data (required) - Dictionary with financial data in the format {"Category1": {"2022": 100, "2021": 90}, ...}
  chart_type (optional) - Type of chart to create (bar, line, pie)
  title (optional) - Title for the visualization
  output_path (optional) - Where to save the generated visualization
  compare_years (optional) - Whether to show year-over-year comparison
"""

# Define custom tools
CUSTOM_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_file_contents",
            "description": "Searches through large documents and retrieves the most relevant text chunks based on semantic or keyword search",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_name": {
                        "type": "string",
                        "description": "Path to the document file to search (supports PDF or text files)",
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query to find relevant information in the document",
                    },
                    "retrieval_method": {
                        "type": "string",
                        "description": "Method used for retrieval: 'bm25' (keyword-based) or 'embedding' (semantic search)",
                        "enum": ["bm25", "embedding"],
                        "default": "bm25"
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific keywords to search for (only used with bm25 method). More precise than using the query alone."
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of text chunks to return. Higher values return more content, useful for complex queries.",
                        "default": 5
                    },
                    "chunk_size": {
                        "type": "integer",
                        "description": "Size of each text chunk in characters. Larger chunks provide more context but may reduce precision.",
                        "default": 3000
                    }
                },
                "required": ["document_name", "query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "visualize_financial_data",
            "description": "Creates visualizations for financial data extracted from documents",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "Dictionary with categories/regions as keys and values as numeric data",
                    },
                    "chart_type": {
                        "type": "string",
                        "description": "Type of chart to create",
                        "enum": ["bar", "line", "pie"],
                        "default": "bar"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title for the visualization",
                        "default": "Financial Data Visualization"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Where to save the generated visualization",
                        "default": "visualization.png"
                    },
                    "compare_years": {
                        "type": "boolean",
                        "description": "Whether to show year-over-year comparison",
                        "default": True
                    }
                },
                "required": ["data"],
            },
        },
    }
]