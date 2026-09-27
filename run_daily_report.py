import sys
import datetime
import subprocess

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def run_step(number, title, script):

    print("\n" + "=" * 70)
    print(f"[{number}/5] {title}")
    print("=" * 70)

    result = subprocess.run(
        [sys.executable, script]
    )

    if result.returncode != 0:
        print(f"\n❌ {script} failed.")
        print(f"Exit code: {result.returncode}")
        sys.exit(result.returncode)

    print(f"\n✅ {title} completed.")


def main():

    start = datetime.datetime.now()

    print("=" * 70)
    print("🇮🇳 DAILY INDIAN MARKET INTELLIGENCE AGENT")
    print("=" * 70)

    # 1. Research
    run_step(
        1,
        "Running AI Research Agent",
        "research_agent.py"
    )

    # 2. Research brief
    run_step(
        2,
        "Creating Research Brief",
        "research_brief.py"
    )

    # 3. Verification
    run_step(
        3,
        "Verifying Research",
        "verify_research.py"
    )

    # 4. Final report
    run_step(
        4,
        "Building Final Report",
        "final_report.py"
    )

    # 5. Email
    print("\n" + "=" * 70)
    print("[5/5] Sending Report by Email")
    print("=" * 70)

    from email_report import send_report

    send_report()

    print("\n✅ Email sent successfully.")

    elapsed = datetime.datetime.now() - start

    print("\n" + "=" * 70)
    print("🎉 COMPLETE AI PIPELINE FINISHED!")
    print("=" * 70)

    print(f"\nStarted : {start}")
    print(f"Finished: {datetime.datetime.now()}")
    print(f"Time    : {elapsed}")

    print("\n📄 Final report:")
    print("   daily_market_report.md")

    print("\n📧 Report sent to email.")


if __name__ == "__main__":
    main()