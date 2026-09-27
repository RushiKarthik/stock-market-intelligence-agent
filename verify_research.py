import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()


def load_files():

    with open("agent_research.json", "r", encoding="utf-8") as f:
        research = json.load(f)

    with open("research_brief.md", "r", encoding="utf-8") as f:
        brief = f.read()

    return research, brief


def compact_research(data):
    """
    Keep only useful textual evidence from the research.
    This prevents the Groq request from becoming too large.
    """

    useful = []

    def walk(obj):

        if isinstance(obj, dict):

            for key, value in obj.items():

                key_lower = str(key).lower()

                # Keep fields that are useful for verification
                if any(word in key_lower for word in [
                    "title",
                    "headline",
                    "source",
                    "link",
                    "url",
                    "summary",
                    "description",
                    "content",
                    "price",
                    "value",
                    "change",
                    "percent",
                    "level",
                    "date",
                    "category"
                ]):

                    if isinstance(value, (str, int, float, bool)):
                        useful.append(
                            f"{key}: {value}"
                        )

                if isinstance(value, (dict, list)):
                    walk(value)

        elif isinstance(obj, list):

            for item in obj:
                walk(item)

    walk(data)

    # Remove duplicates
    seen = set()
    result = []

    for item in useful:

        if item not in seen:
            seen.add(item)
            result.append(item)

    # Limit size
    return "\n".join(result)[:18000]


def verify_research(research, brief):

    print("\n🔍 Verifying research brief...")

    compact_data = compact_research(research)

    # Keep the brief below a safe size
    brief_for_ai = brief[:12000]

    print(
        f"📦 Evidence sent to AI: "
        f"{len(compact_data)} characters"
    )

    print(
        f"📋 Brief sent to AI: "
        f"{len(brief_for_ai)} characters"
    )

    prompt = f"""
You are a strict fact checker for an Indian market
intelligence system.

Verify the FACT claims in the research brief using ONLY
the supplied evidence.

Do NOT use outside knowledge.

Do NOT verify ANALYSIS as fact.

For each important factual claim:

VERIFIED
= evidence directly supports it.

PARTIALLY VERIFIED
= evidence supports only part of it.

UNVERIFIED
= evidence does not support it.

Return:

# RESEARCH VERIFICATION

## Verified

- Claim:
- Evidence:
- Source:

## Partially Verified

- Claim:
- Evidence:
- Issue:

## Unverified

- Claim:
- Reason:

## Verification Summary

- Verified: X
- Partially verified: X
- Unverified: X


================ EVIDENCE ================

{compact_data}


================ RESEARCH BRIEF ================

{brief_for_ai}
"""

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict evidence-based "
                    "fact checker. Never invent evidence."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    return response.choices[0].message.content


def main():

    print("=" * 70)
    print("🔍 RESEARCH VERIFICATION")
    print("=" * 70)

    research, brief = load_files()

    print("\n📋 Research brief loaded:")
    print(f"   Characters: {len(brief)}")

    print("\n📦 Raw research loaded.")

    verification = verify_research(
        research,
        brief
    )

    print("\n" + "=" * 70)
    print(verification)
    print("=" * 70)

    with open(
        "research_verification.md",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(verification)

    print("\n✅ Verification saved to research_verification.md")


if __name__ == "__main__":
    main()