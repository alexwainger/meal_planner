"""
Module for sending email with weekly meal plan and shopping list.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config


def clean_ingredient_text(text):
    # Remove ".0" from whole numbers
    import re
    text = re.sub(r'(\d+)\.0\b', r'\1', text)

    # Remove "count" unit
    text = re.sub(r'\bcount\b', '', text)

    # Clean up extra spaces
    return ' '.join(text.split())

def create_email_content(recipes, shopping_list, test_mode=False):
    """
    Create the email content with recipes and shopping list.
    
    Args:
        recipes (list): List of recipe dictionaries.
        shopping_list (dict): Dictionary with 'regular' and 'staples' lists.
        test_mode (bool): If True, add test mode indicator to email.
        
    Returns:
        str: HTML content for the email.
    """

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
    
    # Display recipes with their indices
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
    
    # Regular items
    if shopping_list["regular"]:
        html += """
            <h3>Items to Buy:</h3>
            <ul class="regular">
        """
        for item in shopping_list["regular"]:
            # Split the item to separate the ingredient from the recipe sources
            parts = item.split(" [")
            if len(parts) > 1:
                ingredient_part = clean_ingredient_text(parts[0])
                recipe_sources = "[" + parts[1]
                html += f"            <li>{ingredient_part} <span class=\"recipe-source\">{recipe_sources}</span></li>\n"
            else:
                html += f"            <li>{clean_ingredient_text(item)}</li>\n"
        html += "            </ul>\n"
    
    # Staple items
    if shopping_list["staples"]:
        html += """
            <h3 class="staples">Staple Items (Check if needed):</h3>
            <ul class="staples">
        """
        for item in shopping_list["staples"]:
            # Split the item to separate the ingredient from the recipe sources
            parts = item.split(" [")
            if len(parts) > 1:
                ingredient_part = clean_ingredient_text(parts[0])
                recipe_sources = "[" + parts[1]
                html += f"            <li>{ingredient_part} <span class=\"recipe-source\">{recipe_sources}</span></li>\n"
            else:
                html += f"            <li>{clean_ingredient_text(item)}</li>\n"
        html += "            </ul>\n"
    
    html += """
        </div>
        
        <p>Bon appétit!</p>
    </body>
    </html>
    """
    
    return html


def create_plain_text_content(recipes, shopping_list, test_mode=False):
    """
    Create plain text version of the email content.
    
    Args:
        recipes (list): List of recipe dictionaries.
        shopping_list (dict): Dictionary with 'regular' and 'staples' lists.
        test_mode (bool): If True, add test mode indicator to email.
        
    Returns:
        str: Plain text content for the email.
    """
    test_indicator = " [TEST MODE]" if test_mode else ""
    
    text = f"MWAH Weekly Meal Plan{test_indicator} - {datetime.now().strftime('%b %d, %Y')}\n\n"
    
    if test_mode:
        text += "TEST MODE: This is a test email sent only to wainger25@gmail.com\n\n"
    
    text += "This Week's Recipes:\n"
    for i, recipe in enumerate(recipes, 1):
        text += f"{i}. {recipe['name']}: {recipe['link']}\n"
    
    text += "\nShopping List:\n"
    
    # Regular items
    if shopping_list["regular"]:
        text += "\nItems to Buy:\n"
        for item in shopping_list["regular"]:
            text += f"- {item}\n"
    
    # Staple items
    if shopping_list["staples"]:
        text += "\nStaple Items (Check if needed):\n"
        for item in shopping_list["staples"]:
            text += f"- {item}\n"
    
    text += "\nBon appétit!"
    
    return text


def send_email(recipes, shopping_list, test_mode=False):
    """
    Send email with recipes and shopping list.
    
    Args:
        recipes (list): List of recipe dictionaries.
        shopping_list (dict): Dictionary with 'regular' and 'staples' lists.
        test_mode (bool): If True, only send to wainger25@gmail.com for testing.
        
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        # Determine email recipients
        if test_mode:
            recipients = ["wainger25@gmail.com"]
        else:
            recipients = config.EMAIL_RECIPIENTS
        
        # Create message container
        msg = MIMEMultipart('alternative')
        test_indicator = " [TEST MODE]" if test_mode else ""
        msg['Subject'] = f"MWAH Weekly Meal Plan{test_indicator} - {datetime.now().strftime('%b %d, %Y')}"
        msg['From'] = config.EMAIL_SENDER
        msg['To'] = ", ".join(recipients)
        
        # Create the plain text and HTML versions of the message
        text_content = create_plain_text_content(recipes, shopping_list, test_mode)
        html_content = create_email_content(recipes, shopping_list, test_mode)
        
        # Attach both parts
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send the email via Gmail SMTP
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