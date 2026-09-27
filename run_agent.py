import subprocess
import sys
import time


def run_step(title, command):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    result = subprocess.run(
        [sys.executable, command],
        capture_output=False
    )

    if result.returncode != 0:
        print(f"\n❌ {command} failed.")
        print(f"Exit code: {result.returncode}")
        return False

    print(f"\n✅ {command} completed.")
    return True


def main():

    start_time = time.time()

    print("\n" + "=" * 70)
    print("🇮🇳 AI INDIAN MARKET INTELLIGENCE AGENT")
    print("=" * 70)

    print("\n🚀 Starting complete pipeline...")


    # --------------------------------------------------
    # 1. Research planning + collection
    # --------------------------------------------------

    if not run_step(
        "STEP 1 — AI RESEARCH PLANNING + DATA COLLECTION",
        "research_agent.py"
    ):
        return


    # --------------------------------------------------
    # 2. AI research brief
    # --------------------------------------------------

    if not run_step(
        "STEP 2 — AI RESEARCH BRIEF",
        "research_brief.py"
    ):
        return


    # --------------------------------------------------
    # 3. Verification
    # --------------------------------------------------

    if not run_step(
        "STEP 3 — RESEARCH VERIFICATION",
        "verify_research.py"
    ):
        return


    # --------------------------------------------------
    # 4. Final report
    # --------------------------------------------------

    if not run_step(
        "STEP 4 — FINAL MARKET REPORT",
        "final_report.py"
    ):
        return


    # --------------------------------------------------
    # Complete
    # --------------------------------------------------

    elapsed = round(time.time() - start_time, 2)

    print("\n" + "=" * 70)
    print("🎉 COMPLETE AI PIPELINE FINISHED")
    print("=" * 70)

    print(f"\n⏱️ Total execution time: {elapsed} seconds")

    print("\nGenerated files:")

    print("   📦 agent_research.json")
    print("   📋 research_brief.md")
    print("   🔍 research_verification.md")
    print("   📝 daily_market_report.md")

    print("\n✅ Pipeline completed successfully.")


if __name__ == "__main__":
    main()