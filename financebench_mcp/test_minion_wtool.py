from minions.minion_wtools import MinionToolCalling
from minions.clients.openai import OpenAIClient
from minions.clients.ollama import OllamaClient
from PyPDF2 import PdfReader
from custom_functions import *
from custom_function_descriptions import *
import os
from typing import List
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

os.chdir('financebench_data')


TEST_QUERIES = [
    # Simple retrieval queries
    "Find Apple's total revenue for 2022 and compare it to 2021.",
    "Find Apple's total debt and shareholders' equity for 2022 and calculate the debt-to-equity ratio.",
    "Identify the top 3 risk factors mentioned in Apple's 10-K and provide a short summary of each.",
    
    # Hybrid queries (retrieval + visualization)
    "Extract Apple's R&D expenses for 2022 and 2021, then create a simple bar chart comparing the two years.",
    "Find the geographic distribution of Apple's net sales for 2022, then create a pie chart showing the percentage breakdown by region."
]

# More generic context pairs
TEST_CONTEXTS = [
    # For simple retrieval queries
    ["Search Local Filesystem. Document is in the current directory. Use relative path.", f"We are in the following directory {os.getcwd()}"],
    ["Search Local Filesystem. Document is in the current directory. Use relative path.", f"We are in the following directory {os.getcwd()}"],
    ["Search Local Filesystem. Document is in the current directory. Use relative path.", f"We are in the following directory {os.getcwd()}"],
    
    # For hybrid queries
    ["Search Local Filesystem and use visualization financial tools for analysis. Use relative path.", f"We are in the following directory {os.getcwd()}", "REMEMBER TO INVOKE THE VISUALIZATION TOOLS"],
    ["Search Local Filesystem and use visualization financial tools for analysis. Use relative path.", f"We are in the following directory {os.getcwd()}", "REMEMBER TO INVOKE THE VISUALIZATION TOOLS"],
]


# Define custom tool executors
CUSTOM_TOOL_EXECUTORS = {
    "search_file_contents": search_file_contents,
    "visualize_financial_data": visualize_financial_data
}


remote_client = OpenAIClient(model_name="gpt-4o")

local_client = OllamaClient(model_name="llama3.2:latest", tool_calling=True)

# Initialize the protocol with the custom tool information
protocol = MinionToolCalling(
    local_client=local_client, 
    remote_client=remote_client,
    custom_tools=CUSTOM_TOOLS,
    custom_tool_executors=CUSTOM_TOOL_EXECUTORS,
    custom_tool_descriptions=CUSTOM_TOOL_DESCRIPTIONS
)

for i in range(len(TEST_QUERIES)):
    for j in range(5):
        try:
            output = protocol(
                task=TEST_QUERIES[i],
                context=TEST_CONTEXTS[i],
                max_rounds=5
            )
            print(f"Query {i} and round {j} completed successfully")
        except Exception as e:
            print(f"Error on query {i} and round {j}: {e}")

