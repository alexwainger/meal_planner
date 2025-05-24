"""
Configuration settings for the meal planner application.
"""

# Google Sheets settings
# GOOGLE_CREDENTIALS_FILE = "credentials.json"  # Downloaded from Google Cloud Console
SERVICE_ACCOUNT_FILE = "service-account-key.json"
# TOKEN_FILE = "token.json"  # Will be created automatically after first login
SPREADSHEET_ID = "1BlkZKhtEegnxb2KsTRoBk--rhuhmUbfqooOM4H-10bw"  # The ID of your Google Sheet
RECIPES_SHEET_NAME = "Recipes"  # Name of the sheet containing recipes
INGREDIENTS_SHEET_NAME = "Ingredients"  # Name of the sheet containing ingredients
HISTORY_SHEET_NAME = "History"  # Name of the sheet containing selection history

# Local file paths (kept for backward compatibility, but no longer used)
HISTORY_FILE = "data/history.csv"

# Email settings
EMAIL_SENDER = "mwahmeals@gmail.com"
EMAIL_PASSWORD = "tgxo vamd qihe qxud"  # App password for Gmail (not the actual password)
EMAIL_RECIPIENTS = ["wainger25@gmail.com", "marcyhuang@gmail.com", "mylesbkeating@gmail.com"]

# Recipe selection settings
NUM_RECIPES_PER_WEEK = 3
REPEAT_WINDOW_DAYS = 30  # Don't repeat recipes within this many days

# Scheduling
# SCHEDULE_DAY = "Sunday"  # Day of the week to send meal plan
# SCHEDULE_TIME = "18:00"  # Time to send meal plan (24-hour format)