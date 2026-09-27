import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()


def plan_research(request):

    print("\n🧠 Creating research plan...")

    prompt = f"""
You are the research planner for an Indian stock market
intelligence system.

User request:
{request}

Decide which research areas are required.

Available research areas:

1. market
   - Nifty 50
   - Sensex
   - Bank Nifty
   - India VIX

2. global
   - US markets
   - Asian markets
   - crude oil
   - gold
   - USD/INR
   - other global market cues

3. news
   - Indian company news
   - earnings
   - orders
   - acquisitions
   - RBI
   - SEBI
   - government policy
   - sector developments

For a complete daily or morning Indian market
intelligence report, all three areas are required.

Return ONLY valid JSON in exactly this format:

{{
    "market": true,
    "global": true,
    "news": true
}}

Do not add explanations.
Do not use markdown.
"""


    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise research planning "
                    "assistant. Return valid JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.0
    )


    result = response.choices[0].message.content

    print("\n🤖 AI research plan:")
    print(result)


    # Convert AI response into Python dictionary

    try:

        plan = json.loads(result)

        print("\n" + "=" * 60)
        print("🔎 RESEARCH PLAN")
        print("=" * 60)

        print(
            f"Market : {plan.get('market')}"
        )

        print(
            f"Global : {plan.get('global')}"
        )

        print(
            f"News   : {plan.get('news')}"
        )

        return plan

    except json.JSONDecodeError:

        print("\n❌ AI did not return valid JSON.")

        return None


if __name__ == "__main__":

    plan_research(
        "Prepare a complete morning Indian stock "
        "market intelligence report."
    )