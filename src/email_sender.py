"""
Module for sending email with weekly meal plan and shopping list.
"""

import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config


def clean_ingredient_text(text):
    """Remove '.0' from whole numbers and 'count' unit, clean up whitespace."""
    text = re.sub(r'(\d+)\.0\b', r'\1', text)
    text = re.sub(r'\bcount\b', '', text)
    return ' '.join(text.split())


def _render_items_html(items):
    """Render a list of shopping list items as HTML <li> elements."""
    html = ""
    for item in items:
        ingredient = clean_ingredient_text(item["text"])
        if item["sources"]:
            source_str = f"[{', '.join(map(str, item['sources']))}]"
            html += f'            <li>{ingredient} <span class="recipe-source">{source_str}</span></li>\n'
        else:
            html += f"            <li>{ingredient}</li>\n"
    return html


def create_email_content(recipes, shopping_list, test_mode=False):
    """Create HTML email content with recipes and shopping list."""
    test_indicator = " [TEST MODE]" if test_mode else ""

    html = f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 15px;
                background-color: #ffffff;
                color: #333333;
                font-size: 16px;
            }}
            h1, h2, h3 {{
                color: #444444;
                margin: 20px 0 10px;
            }}
            ul {{
                margin-top: 10px;
                padding-left: 20px;
            }}
            .recipe {{
                margin-bottom: 12px;
            }}
            .recipe-list {{
                list-style: none;
                padding-left: 0;
                margin: 0;
            }}
            .shopping-list {{
                margin-top: 30px;
            }}
            .regular {{
                list-style: none;
            }}
            .staples {{
                list-style: none;
                margin-top: 20px;
                color: #666666;
            }}
            .recipe-index {{
                font-weight: bold;
                color: #555555;
            }}
            .recipe-source {{
                color: #888888;
                font-style: italic;
            }}
            .test-mode {{
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
                padding: 10px;
                margin-bottom: 20px;
                border-radius: 4px;
            }}
            a {{
                color: #333333;
                text-decoration: underline;
            }}
            @media only screen and (max-width: 600px) {{
                body {{
                    font-size: 18px;
                    padding: 10px;
                }}
            }}
        </style>
    </head>
    <body>
        <h1>MWAH Weekly Meal Plan{test_indicator} - {datetime.now().strftime('%b %d, %Y')}</h1>

        {f'<div class="test-mode"><strong>TEST MODE:</strong> This is a test email sent only to wainger25@gmail.com</div>' if test_mode else ''}

        <h2>This Week's Recipes:</h2>
        <ul class="recipe-list">
    """

    for i, recipe in enumerate(recipes, 1):
        html += f"""
            <li class="recipe">
                <span class="recipe-index">{i}.</span> <a href="{recipe['link']}">{recipe['name']}</a>
            </li>
        """

    html += """
        </ul>

        <div class="shopping-list">
            <h2>Shopping List:</h2>
    """

    if shopping_list["regular"]:
        html += '            <h3>Items to Buy:</h3>\n            <ul class="regular">\n'
        html += _render_items_html(shopping_list["regular"])
        html += "            </ul>\n"

    if shopping_list["staples"]:
        html += '            <h3 class="staples">Staple Items (Check if needed):</h3>\n            <ul class="staples">\n'
        html += _render_items_html(shopping_list["staples"])
        html += "            </ul>\n"

    html += """
        </div>

        <p>Bon appétit!</p>
    </body>
    </html>
    """

    return html


def create_plain_text_content(recipes, shopping_list, test_mode=False):
    """Create plain text version of the email content."""
    test_indicator = " [TEST MODE]" if test_mode else ""

    text = f"MWAH Weekly Meal Plan{test_indicator} - {datetime.now().strftime('%b %d, %Y')}\n\n"

    if test_mode:
        text += "TEST MODE: This is a test email sent only to wainger25@gmail.com\n\n"

    text += "This Week's Recipes:\n"
    for i, recipe in enumerate(recipes, 1):
        text += f"{i}. {recipe['name']}: {recipe['link']}\n"

    text += "\nShopping List:\n"

    if shopping_list["regular"]:
        text += "\nItems to Buy:\n"
        for item in shopping_list["regular"]:
            line = clean_ingredient_text(item["text"])
            if item["sources"]:
                line += f" [{', '.join(map(str, item['sources']))}]"
            text += f"- {line}\n"

    if shopping_list["staples"]:
        text += "\nStaple Items (Check if needed):\n"
        for item in shopping_list["staples"]:
            line = clean_ingredient_text(item["text"])
            if item["sources"]:
                line += f" [{', '.join(map(str, item['sources']))}]"
            text += f"- {line}\n"

    text += "\nBon appétit!"

    return text


def send_email(recipes, shopping_list, test_mode=False):
    """Send email with recipes and shopping list. Returns True on success."""
    try:
        if test_mode:
            recipients = ["wainger25@gmail.com"]
        else:
            recipients = config.EMAIL_RECIPIENTS

        msg = MIMEMultipart('alternative')
        test_indicator = " [TEST MODE]" if test_mode else ""
        msg['Subject'] = f"MWAH Weekly Meal Plan{test_indicator} - {datetime.now().strftime('%b %d, %Y')}"
        msg['From'] = config.EMAIL_SENDER
        msg['To'] = ", ".join(recipients)

        text_content = create_plain_text_content(recipes, shopping_list, test_mode)
        html_content = create_email_content(recipes, shopping_list, test_mode)

        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.sendmail(config.EMAIL_SENDER, recipients, msg.as_string())

        if test_mode:
            print("Test email sent successfully to wainger25@gmail.com!")
        else:
            print("Email sent successfully!")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
