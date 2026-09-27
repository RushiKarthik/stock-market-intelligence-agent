import json
from datetime import datetime


def load_research():
    with open("research_data.json", "r", encoding="utf-8") as file:
        return json.load(file)


def generate_report(research):

    market = research["market"]
    news = research["news"]
    global_data = research["global"]

    report = []

    # Header
    report.append("🇮🇳 DAILY INDIAN STOCK MARKET INTELLIGENCE")
    report.append("=" * 70)
    report.append(
        f"Generated: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
    )

    # --------------------------------------------------
    # 1. MARKET SNAPSHOT
    # --------------------------------------------------

    report.append("\n📊 1. INDIAN MARKET SNAPSHOT")
    report.append("-" * 70)

    for name, data in market.items():

        if data["status"] == "OK":

            direction = "↑" if data["change_percent"] > 0 else "↓"

            report.append(
                f"{name}: {data['value']} "
                f"{direction} {abs(data['change_percent'])}%"
            )

        else:
            report.append(f"{name}: {data['status']}")

    # --------------------------------------------------
    # 2. TOP INDIAN DEVELOPMENTS
    # --------------------------------------------------

    report.append("\n📰 2. TOP INDIAN MARKET DEVELOPMENTS")
    report.append("-" * 70)

    if not news:
        report.append("No recent Indian market news found.")

    else:

        for i, article in enumerate(news[:10], 1):

            report.append(f"\n{i}. {article['title']}")
            report.append(
                f"   Relevance Score: {article.get('relevance_score', 0)}"
            )
            report.append(
                f"   Published: {article.get('published', 'Unknown')}"
            )
            report.append(
                f"   Source Category: {article.get('source', 'Unknown')}"
            )
            report.append(f"   Link: {article.get('link', '')}")

    # --------------------------------------------------
    # 3. GLOBAL CONTEXT
    # --------------------------------------------------

    report.append("\n🌎 3. GLOBAL CONTEXT")
    report.append("-" * 70)
    report.append(
        "Global markets are shown only as supporting context "
        "for the Indian market."
    )

    for name, data in global_data.items():

        if data["status"] == "OK":

            direction = "↑" if data["change_percent"] > 0 else "↓"

            report.append(
                f"{name}: {data['value']} "
                f"{direction} {abs(data['change_percent'])}%"
            )

    # --------------------------------------------------
    # 4. STOCKS / COMPANIES TO WATCH
    # --------------------------------------------------

    report.append("\n👀 4. COMPANIES / STOCKS TO WATCH")
    report.append("-" * 70)

    report.append(
        "Company-level watchlist will be added after "
        "AI analysis and company-name extraction are implemented."
    )

    # --------------------------------------------------
    # 5. EDUCATIONAL SECTION
    # --------------------------------------------------

    report.append("\n🧠 5. WHAT TO LEARN TODAY")
    report.append("-" * 70)

    report.append(
        "• Market movement should be connected to actual catalysts "
        "rather than assumed from price movement."
    )

    report.append(
        "• News relevance and market impact are not always the same."
    )

    report.append(
        "• Global markets can influence Indian markets through "
        "capital flows, commodities and investor sentiment."
    )

    # --------------------------------------------------
    # 6. DISCLAIMER
    # --------------------------------------------------

    report.append("\n⚠️ NOTE")
    report.append("-" * 70)

    report.append(
        "This report is for research and educational purposes only. "
        "It is not financial advice."
    )

    return "\n".join(report)


if __name__ == "__main__":

    research = load_research()

    report = generate_report(research)

    print("\n" + report)

    with open(
        "daily_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    print("\n")
    print("✅ Daily report saved to daily_report.txt")