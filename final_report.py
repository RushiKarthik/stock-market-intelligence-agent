from datetime import datetime


def load_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def build_report(research_brief, verification):

    report = []

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------

    report.append("# 🇮🇳 DAILY INDIAN MARKET INTELLIGENCE")
    report.append("")
    report.append(
        f"**Generated:** "
        f"{datetime.now().strftime('%d %B %Y, %I:%M %p')}"
    )
    report.append("")

    report.append(
        "> **Purpose:** Educational market intelligence. "
        "This report does not provide BUY/SELL recommendations "
        "or guaranteed predictions."
    )

    # --------------------------------------------------
    # 1. AI RESEARCH BRIEF
    # --------------------------------------------------

    report.append("\n## 🧠 1. AI Research Brief\n")

    report.append(research_brief)

    # --------------------------------------------------
    # 2. VERIFICATION
    # --------------------------------------------------

    report.append("\n\n## 🔍 2. Research Verification\n")

    report.append(
        "The following section shows the evidence-verification "
        "result for the research brief."
    )

    report.append("")

    report.append(verification)

    # --------------------------------------------------
    # 3. IMPORTANT RULES
    # --------------------------------------------------

    report.append("\n## ⚠️ 3. Interpretation Rules\n")

    report.append(
        "- **FACT:** Information directly supported by collected research."
    )

    report.append(
        "- **ANALYSIS:** Reasoned interpretation of the available data."
    )

    report.append(
        "- **VERIFIED:** The available research supports the statement."
    )

    report.append(
        "- **PARTIALLY VERIFIED:** Evidence supports only part of the statement."
    )

    report.append(
        "- **UNVERIFIED:** The available research does not support the statement."
    )

    report.append(
        "- Unsupported explanations should not be treated as confirmed facts."
    )

    # --------------------------------------------------
    # 4. DISCLAIMER
    # --------------------------------------------------

    report.append("\n## 📚 4. Educational Use\n")

    report.append(
        "This report is designed to help understand Indian market "
        "movements, global cues, news, market sentiment and possible "
        "relationships between events and prices."
    )

    report.append("")

    report.append(
        "It is not investment advice. Always independently verify "
        "important information before making financial decisions."
    )

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    report.append("\n---")

    report.append(
        f"\nGenerated automatically on "
        f"{datetime.now().strftime('%d-%m-%Y %H:%M')}"
    )

    return "\n".join(report)


def main():

    print("=" * 70)
    print("📝 BUILDING FINAL MARKET REPORT")
    print("=" * 70)

    # New agent pipeline files
    research_brief = load_file(
        "research_brief.md"
    )

    verification = load_file(
        "research_verification.md"
    )

    print("\n✅ Research brief loaded")
    print("✅ Verification loaded")

    final_report = build_report(
        research_brief,
        verification
    )

    print("\n" + "=" * 70)
    print("🇮🇳 FINAL DAILY MARKET REPORT")
    print("=" * 70)

    print(final_report)

    with open(
        "daily_market_report.md",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(final_report)

    print("\n" + "=" * 70)
    print("✅ FINAL REPORT SAVED")
    print("=" * 70)

    print("\n📄 daily_market_report.md")


if __name__ == "__main__":
    main()