# internet_access.py

import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import get_api_key  # Updated import to handle Google API key

def search_internet(query, max_results=5):
    """
    Searches the internet using Google's Custom Search API and returns a summary of the results.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of search results to return.

    Returns:
        str: A concatenated string of search result titles, URLs, and snippets or an error message.
    """
    if not query:
        logging.error("Empty query provided to search_internet function.")
        return "Error: No search query provided."

    try:
        logging.info(f"Initiating Google Custom Search for query: {query}")

        # Retrieve Google API key and Search Engine ID securely
        api_key = get_api_key(api_type="google")
        search_engine_id = get_api_key(api_type="google_search_engine_id")
        # Initialize the Custom Search API
        service = build("customsearch", "v1", developerKey=api_key)

        # Perform the search
        res = service.cse().list(q=query, cx=search_engine_id, num=max_results).execute()

        # Process the results
        items = res.get('items', [])
        if not items:
            logging.info(f"No results found for query: {query}")
            return "No relevant results found."

        results = []
        for item in items:
            title = item.get('title', 'No Title')
            link = item.get('link', 'No Link')
            snippet = item.get('snippet', 'No Snippet')
            results.append(f"**{title}**\n{link}\n{snippet}\n")

        logging.info(f"Found {len(results)} results for query: {query}")
        return "\n".join(results)

    except HttpError as e:
        logging.error(f"HTTP error occurred: {e}")
        return f"An error occurred while performing the search: {e}"
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        return f"An unexpected error occurred: {str(e)}"
