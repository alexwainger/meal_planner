"""
Configuration settings for the meal planner application.
"""

# Google Sheets settings
SERVICE_ACCOUNT_FILE = "service-account-key.json"
SPREADSHEET_ID = "1BlkZKhtEegnxb2KsTRoBk--rhuhmUbfqooOM4H-10bw"  # The ID of your Google Sheet
RECIPES_SHEET_NAME = "Recipes"  # Name of the sheet containing recipes
INGREDIENTS_SHEET_NAME = "Ingredients"  # Name of the sheet containing ingredients
HISTORY_SHEET_NAME = "History"  # Name of the sheet containing selection history

# Local file paths (kept for backward compatibility, but no longer used)
HISTORY_FILE = "data/history.csv"

# Email settings
EMAIL_SENDER = "mwahmeals@gmail.com"
EMAIL_PASSWORD = "tgxo vamd qihe qxud"  # App password for Gmail (not the actual password)
EMAIL_RECIPIENTS = ["wainger25@gmail.com", "marcyhuang@gmail.com", "mylesbkeating@gmail.com", "evans.abraham@gmail.com", "gildeah@gmail.com"]

# Recipe selection settings
NUM_RECIPES_PER_WEEK = 3
REPEAT_WINDOW_DAYS = 30  # Don't repeat recipes within this many days