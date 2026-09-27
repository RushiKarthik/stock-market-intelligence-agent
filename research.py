from market_data import get_market_data
from news import get_news
from global_data import get_global_data
import json


def collect_research():
    print("Collecting Indian market data...")
    market = get_market_data()

    print("Collecting Indian market news...")
    news = get_news()

    print("Collecting global market cues...")
    global_data = get_global_data()

    return {
        "market": market,
        "news": news,
        "global": global_data
    }


def save_research(data):
    with open("research_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    research = collect_research()

    save_research(research)

    print("\nResearch collected successfully.")
    print("Saved to research_data.json")

    print(f"Indian market indicators: {len(research['market'])}")
    print(f"Indian news articles: {len(research['news'])}")
    print(f"Global indicators: {len(research['global'])}")