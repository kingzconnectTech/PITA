import logging
import webbrowser

logger = logging.getLogger("Lucy-BrowserControl")

class BrowserController:
    """
    Handles browser operations.
    """
    def __init__(self):
        logger.info("Browser Controller initialized.")

    def open_url(self, url: str) -> str:
        """Opens a URL in the default browser."""
        logger.info(f"Opening URL: '{url}'")
        webbrowser.open(url)
        return f"Opening '{url}' now."

    def search(self, query: str) -> str:
        """Searches the web."""
        logger.info(f"Searching: '{query}'")
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        return f"Searching Google for '{query}'."
