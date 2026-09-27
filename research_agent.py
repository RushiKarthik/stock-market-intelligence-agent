import json

from agent_tools import TOOLS
from research_planner import plan_research


# --------------------------------------------------
# Research Agent
# --------------------------------------------------

def run_research(request):

    print("\n" + "=" * 70)
    print("🔎 RESEARCH AGENT")
    print("=" * 70)

    # --------------------------------------------------
    # STEP 1 — Ask AI what research is required
    # --------------------------------------------------

    plan = plan_research(request)

    if not plan:
        print("\n❌ Research plan could not be created.")
        return None


    research = {}


    # --------------------------------------------------
    # STEP 2 — Execute Market research if requested
    # --------------------------------------------------

    if plan.get("market") is True:

        print("\n📊 Collecting Indian market data...")

        try:

            research["market"] = TOOLS["get_market_data"]()

            print("✅ Market data collected")

        except Exception as error:

            print("❌ Market data failed:", error)

            research["market"] = {
                "error": str(error)
            }


    # --------------------------------------------------
    # STEP 3 — Execute Global research if requested
    # --------------------------------------------------

    if plan.get("global") is True:

        print("\n🌎 Collecting global market data...")

        try:

            research["global"] = TOOLS["get_global_data"]()

            print("✅ Global data collected")

        except Exception as error:

            print("❌ Global data failed:", error)

            research["global"] = {
                "error": str(error)
            }


    # --------------------------------------------------
    # STEP 4 — Execute News research if requested
    # --------------------------------------------------

    if plan.get("news") is True:

        print("\n📰 Collecting Indian market news...")

        try:

            research["news"] = TOOLS["get_news"]()

            print("✅ News collected")

        except Exception as error:

            print("❌ News collection failed:", error)

            research["news"] = []


    # --------------------------------------------------
    # STEP 5 — Save research results
    # --------------------------------------------------

    with open(
        "agent_research.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            research,
            file,
            indent=2,
            ensure_ascii=False
        )


    # --------------------------------------------------
    # STEP 6 — Display summary
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("📦 RESEARCH COLLECTION COMPLETE")
    print("=" * 70)

    print(
        f"\nResearch sections collected: "
        f"{len(research)}"
    )

    for section in research:

        print(f"   ✅ {section}")

    print("\n📁 Saved to: agent_research.json")

    return research


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    run_research(
        "Prepare a complete morning Indian stock "
        "market intelligence report."
    )