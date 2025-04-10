from minions.utils.retrievers import bm25_retrieve_top_k_chunks, embedding_retrieve_top_k_chunks
from minions.minions import chunk_by_section
from typing import List, Optional

def read_file(file_path):
    """Read the contents of a file.

    Args:
        file_path: Path to the file to read

    Returns:
        Contents of the file as a string
    """
    import os

    # Get file extension
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    try:
        # Handle PDF files
        if ext == ".pdf":
            try:
                import PyPDF2

                with open(file_path, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page.extract_text()
                with open(f"page_text.txt", "w") as f:
                    f.write(text)
                return text
            except ImportError:
                return "Error: PyPDF2 library not installed. Install with 'pip install PyPDF2' to read PDF files."
            except Exception as e:
                return f"Error reading PDF file: {str(e)}"

        # Handle text files
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Try binary mode if UTF-8 fails
        try:
            with open(file_path, "rb") as f:
                return f"Binary file, first 1000 bytes: {f.read(1000)}"
        except Exception as e:
            return f"Error reading file as binary: {str(e)}"
    except Exception as e:
        return f"Error reading file: {str(e)}"




def search_file_contents(
        document_name: str,
        query: str,
        retrieval_method: str = "bm25",
        keywords: Optional[List[str]] = None,
        top_k: int = 5,
        chunk_size: int = 3000
) -> List[str]:
    """
    Search through a large document and retrieve the most relevant text chunks based on a query.
    This function breaks the document into chunks and finds the sections most relevant to your query.
    
    Args:
        document_name (str): Path to the document file to search (supports PDF or text files)
        query (str): Search query to find relevant information in the document
        retrieval_method (str): Method used for retrieval
            - "bm25": Keyword-based search, better for finding exact matches
            - "embedding": Semantic search, better for finding conceptually related content
        keywords (list): Specific keywords to search for (MUST BE USED WITH BM25 METHOD)
            Providing targeted keywords can improve precision when using the bm25 method
        top_k (int): Number of text chunks to return
            Higher values return more content, useful for complex queries or ensuring comprehensive coverage
        chunk_size (int): Size of each text chunk in characters
            Larger chunks provide more context but may reduce precision
            Smaller chunks are more precise but may miss broader context
    
    Returns:
        List of the most relevant text chunks from the document
    """

    # int type enforcement
    top_k = int(top_k)
    chunk_size = int(chunk_size)

    # read the file
    text = read_file(document_name)
    
    # chunk the text
    chunks = chunk_by_section(text, max_chunk_size=chunk_size)

    
    # search the chunks
    if retrieval_method == "bm25":
        # If no keywords provided, use query words as keywords
        if keywords is None:
            keywords = query.split()
        return bm25_retrieve_top_k_chunks(
            keywords=keywords,
            chunks=chunks,
            weights={},
            k=top_k
        )
    else:
        return embedding_retrieve_top_k_chunks(
            queries=[query],  # Function expects a list of queries
            chunks=chunks,
            k=top_k
        )

def visualize_financial_data(
    data: dict,
    chart_type: str = "bar",
    title: str = "Financial Data Visualization",
    output_path: str = "visualization.png",
    compare_years: bool = True
) -> str:
    """
    Creates visualizations for financial data extracted from documents.
    
    Args:
        data: Dictionary with categories/regions as keys and values as numeric data
             Format: {"Category1": {"2022": 100, "2021": 90}, "Category2": {"2022": 200, "2021": 180}}
        chart_type: Type of chart to create (bar, line, pie)
        title: Title for the visualization
        output_path: Where to save the generated visualization
        compare_years: Whether to show year-over-year comparison
        
    Returns:
        Path to the saved visualization file
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    plt.figure(figsize=(12, 8))
    
    if chart_type == "bar":
        # Extract years and categories
        categories = list(data.keys())
        if compare_years and all(isinstance(v, dict) for v in data.values()):
            years = set()
            for category_data in data.values():
                years.update(category_data.keys())
            years = sorted(years)
            
            # Set up grouped bar chart
            x = np.arange(len(categories))
            width = 0.8 / len(years)
            
            for i, year in enumerate(years):
                values = [data[category].get(year, 0) for category in categories]
                plt.bar(x + i*width - width*len(years)/2 + width/2, values, width, label=year)
            
            plt.xlabel('Categories')
            plt.ylabel('Values (in millions $)')
            plt.title(title)
            plt.xticks(x, categories, rotation=45, ha="right")
            plt.legend()
            
        else:
            # Simple bar chart for single year
            values = [data[category] if not isinstance(data[category], dict) else 
                      list(data[category].values())[0] for category in categories]
            plt.bar(categories, values)
            plt.xlabel('Categories')
            plt.ylabel('Values (in millions $)')
            plt.title(title)
            plt.xticks(rotation=45, ha="right")
    
    elif chart_type == "pie":
        # Extract data for pie chart
        categories = list(data.keys())
        if all(isinstance(v, dict) for v in data.values()):
            # Use the most recent year for pie chart
            latest_year = max(next(iter(data.values())).keys())
            values = [data[category].get(latest_year, 0) for category in categories]
        else:
            values = [data[category] if not isinstance(data[category], dict) else 
                     list(data[category].values())[0] for category in categories]
        
        plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title(title)
    
    elif chart_type == "line":
        # Extract years for line chart
        if all(isinstance(v, dict) for v in data.values()):
            categories = list(data.keys())
            for category in categories:
                years = sorted(data[category].keys())
                values = [data[category][year] for year in years]
                plt.plot(years, values, marker='o', label=category)
            
            plt.xlabel('Year')
            plt.ylabel('Values (in millions $)')
            plt.title(title)
            plt.legend()
        else:
            plt.text(0.5, 0.5, "Line chart requires year-over-year data", 
                     horizontalalignment='center', verticalalignment='center')
    
    plt.tight_layout()
    print(f"Saving visualization to {output_path}")
    plt.savefig(output_path)
    plt.close()
    
    return output_path