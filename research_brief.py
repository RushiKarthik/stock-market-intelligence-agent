import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()


# --------------------------------------------------
# STEP 1 — Load collected research
# --------------------------------------------------

def load_research():

    with open(
        "agent_research.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# --------------------------------------------------
# STEP 2 — Create AI research brief
# --------------------------------------------------

def create_research_brief(research):

    print("\n🧠 Creating AI research brief...")

    prompt = f"""
You are a careful Indian stock market research analyst.

Your job is to understand the research data collected by
our research agent and create a concise research brief.

The purpose is EDUCATIONAL market intelligence.

IMPORTANT RULES:

- Do NOT give BUY or SELL recommendations.
- Do NOT give price targets.
- Do NOT make guaranteed predictions.
- Do NOT invent facts, numbers, companies, events or reasons.
- Use ONLY the supplied research data for factual claims.
- If information is missing, say:
  "Not available in supplied data."
- Clearly separate FACT from ANALYSIS.
- Analysis may use general financial knowledge, but it must
  be clearly labelled as ANALYSIS.
- Do not treat analysis as a confirmed fact.

Create the brief using these sections:

# 📋 RESEARCH BRIEF

## 1. Market Overview

Summarize:
- Nifty 50
- Sensex
- Bank Nifty
- India VIX

## 2. Global Context

Summarize the supplied:
- US markets
- Asian markets
- Crude oil
- Gold
- USD/INR

Explain only the potentially relevant connections to Indian markets.

## 3. Important Indian Developments

Identify the most important developments from the supplied
news data.

For each important development include:

### [Development]

**What happened:**
FACT-based summary.

**Why it matters:**
ANALYSIS of potential significance.

**Affected company/sector:**
Only if supported by the supplied data.

**Source:**
Include the supplied source and link.

## 4. Sector Watch

Identify sectors that appear relevant based on the supplied
news.

Do not invent sector impact.

## 5. Key Market Themes

Summarize the major themes visible in the research.

## 6. What To Learn Today

Give 3 useful financial-market concepts that can be learned
from today's research.

For each concept explain it simply.

## 7. Research Limitations

Mention important information that was unavailable,
uncertain, or not confirmed by the supplied data.

Remember:

FACT = directly supported by supplied data.

ANALYSIS = interpretation or general financial context.

Never mix the two.

RESEARCH DATA:

{json.dumps(research, indent=2, ensure_ascii=False)}
"""

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a conservative, evidence-based "
                    "financial research analyst."
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


# --------------------------------------------------
# STEP 3 — Run
# --------------------------------------------------

if __name__ == "__main__":

    research = load_research()

    try:

        brief = create_research_brief(research)

        print("\n" + "=" * 70)
        print("📋 AI RESEARCH BRIEF")
        print("=" * 70)

        print(brief)

        with open(
            "research_brief.md",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(brief)

        print("\n" + "=" * 70)
        print("✅ Research brief saved to research_brief.md")
        print("=" * 70)

    except Exception as error:

        print("\n❌ Research brief generation failed.")
        print("Error:", error)