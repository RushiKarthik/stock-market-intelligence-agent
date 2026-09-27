import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=API_KEY)


def load_research():
    with open("research_data.json", "r", encoding="utf-8") as file:
        return json.load(file)


def analyze_news(research):

    news = research["news"][:15]

    compact_news = []

    for article in news:
        compact_news.append({
            "title": article.get("title", ""),
            "published": article.get("published", ""),
            "source": article.get("source", ""),
            "link": article.get("link", ""),
            "category": article.get("category", ""),
            "relevance_score": article.get("relevance_score", 0)
        })

    prompt = f"""
You are a careful Indian stock market research analyst.

Your job is to analyze the supplied recent news and identify
the most important developments for an Indian investor who wants
to LEARN about markets.

IMPORTANT:

- Focus primarily on Indian markets.
- Do NOT give BUY or SELL recommendations.
- Do NOT give price targets.
- Do NOT predict guaranteed market movements.
- Do NOT invent facts.
- Do NOT invent company names, sectors, numbers, events or reasons.
- Remove duplicate stories covering the same underlying event.
- Rank developments by potential market importance, not simply recency.

SOURCE AND EVIDENCE RULES:

- The supplied headline is the primary evidence.
- The supplied source and link are references to the original article.
- Do not claim that the article confirms information that is not
  present in the supplied data.
- If the supplied information does not establish a reason, write:
  "Reason not confirmed from supplied data."
- Never use speculation disguised as fact.
- General financial knowledge may ONLY appear under ANALYSIS.
- Clearly distinguish FACT from ANALYSIS.

For each development provide:

### 1. [Development title]

**Source:** [source]
**Link:** [link]

**What happened:**
Explain only what is supported by the supplied information.

**Why it matters:**
Explain the potential market significance.

**Affected company/sector:**
Only identify this if supported by the supplied information.
Otherwise write:
"Not established from supplied data."

**FACT:**
- List only directly supported information.

**ANALYSIS:**
- Clearly label interpretation or general financial context.

**Confidence:** High / Medium / Low

IMPORTANT:

If the headline does not establish the reason for a market move,
write exactly:

"Reason not confirmed from supplied data."

Do not invent a reason.

Return ONLY the 5 most important developments.

NEWS DATA:

{json.dumps(compact_news, indent=2, ensure_ascii=False)}
"""

    print("Sending Indian news to Groq...")

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a conservative, evidence-based "
                    "Indian financial research analyst."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    research = load_research()

    try:

        analysis = analyze_news(research)

        print("\n" + "=" * 70)
        print("🧠 AI ANALYSIS — INDIAN MARKET NEWS")
        print("=" * 70)

        print(analysis)

        with open(
            "news_ai_analysis.md",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(analysis)

        print("\n✅ AI analysis saved to news_ai_analysis.md")

    except Exception as error:

        print("\n❌ Groq request failed.")
        print("Error:", error)