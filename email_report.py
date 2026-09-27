import smtplib
import os
import html
import re
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")


def markdown_to_html(markdown):

    text = html.escape(markdown)

    # Headings
    text = re.sub(
        r"^# (.+)$",
        r'<h1>\1</h1>',
        text,
        flags=re.MULTILINE
    )

    text = re.sub(
        r"^## (.+)$",
        r'<h2>\1</h2>',
        text,
        flags=re.MULTILINE
    )

    text = re.sub(
        r"^### (.+)$",
        r'<h3>\1</h3>',
        text,
        flags=re.MULTILINE
    )

    # Bold
    text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<strong>\1</strong>",
        text
    )

    # Horizontal line
    text = re.sub(
        r"^-{3,}$",
        r"<hr>",
        text,
        flags=re.MULTILINE
    )

    # Bullet points
    text = re.sub(
        r"^- (.+)$",
        r"<li>\1</li>",
        text,
        flags=re.MULTILINE
    )

    # Wrap consecutive list items
    text = re.sub(
        r"((?:<li>.*?</li>\s*)+)",
        r"<ul>\1</ul>",
        text
    )

    # Tables — basic Markdown table support
    lines = text.split("\n")

    output = []
    in_table = False

    for line in lines:

        if "|" in line:

            cells = [
                c.strip()
                for c in line.strip().strip("|").split("|")
            ]

            # Skip markdown separator row
            if all(
                re.fullmatch(r"[-: ]+", cell)
                for cell in cells
            ):
                continue

            if not in_table:

                output.append("<table>")
                output.append("<tr>")

                for cell in cells:
                    output.append(
                        f"<th>{cell}</th>"
                    )

                output.append("</tr>")

                in_table = True

            else:

                output.append("<tr>")

                for cell in cells:
                    output.append(
                        f"<td>{cell}</td>"
                    )

                output.append("</tr>")

        else:

            if in_table:

                output.append("</table>")
                in_table = False

            if line.strip():

                # Don't add extra paragraph around HTML tags
                if line.startswith("<h") or line.startswith("<hr") \
                        or line.startswith("<ul") \
                        or line.startswith("</ul"):

                    output.append(line)

                else:

                    output.append(
                        f"<p>{line}</p>"
                    )

    if in_table:
        output.append("</table>")

    return "\n".join(output)


def build_html_email(report):

    body = markdown_to_html(report)

    return f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<style>

body {{
    font-family: Arial, Helvetica, sans-serif;
    background: #f4f6f8;
    color: #202124;
    margin: 0;
    padding: 20px;
}}

.container {{
    max-width: 850px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
}}

h1 {{
    font-size: 26px;
    margin-bottom: 10px;
}}

h2 {{
    margin-top: 28px;
    padding-bottom: 8px;
    border-bottom: 1px solid #ddd;
}}

h3 {{
    margin-top: 20px;
}}

p {{
    line-height: 1.6;
}}

ul {{
    line-height: 1.7;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
}}

th {{
    background: #f1f3f4;
    font-weight: bold;
}}

th, td {{
    padding: 10px;
    border: 1px solid #ddd;
    text-align: left;
}}

hr {{
    border: 0;
    border-top: 1px solid #ddd;
    margin: 25px 0;
}}

strong {{
    font-weight: 700;
}}

.footer {{
    margin-top: 30px;
    padding-top: 15px;
    border-top: 1px solid #ddd;
    font-size: 12px;
    color: #666;
}}

</style>

</head>

<body>

<div class="container">

{body}

<div class="footer">

Generated automatically by your
Indian Market Intelligence Agent.

<br><br>

Educational research only.
Not financial advice.

</div>

</div>

</body>
</html>
"""


def send_report():

    with open(
        "daily_market_report.md",
        "r",
        encoding="utf-8"
    ) as file:

        report = file.read()

    message = EmailMessage()

    message["Subject"] = (
        "🇮🇳 Daily Indian Market Intelligence"
    )

    message["From"] = GMAIL_ADDRESS
    message["To"] = TO_EMAIL

    # Plain text fallback
    message.set_content(report)

    # HTML version
    html_content = build_html_email(report)

    message.add_alternative(
        html_content,
        subtype="html"
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        server.login(
            GMAIL_ADDRESS,
            GMAIL_APP_PASSWORD
        )

        server.send_message(message)

    print("✅ Report emailed successfully!")


if __name__ == "__main__":
    send_report()