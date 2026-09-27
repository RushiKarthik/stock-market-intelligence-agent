from market_data import get_market_data
from global_data import get_global_data
from news import get_news


def market_tool():
    """Get current Indian market indicators."""
    return get_market_data()


def global_tool():
    """Get global market indicators and macro cues."""
    return get_global_data()


def news_tool():
    """Get recent Indian stock-market news."""
    return get_news()


TOOLS = {
    "get_market_data": market_tool,
    "get_global_data": global_tool,
    "get_news": news_tool,
}