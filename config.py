"""
Configuration settings for the meal planner application.
"""

import os

# Google Sheets settings
SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE", "service-account-key.json")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "1BlkZKhtEegnxb2KsTRoBk--rhuhmUbfqooOM4H-10bw")
RECIPES_SHEET_NAME = "Recipes"
INGREDIENTS_SHEET_NAME = "Ingredients"
HISTORY_SHEET_NAME = "History"

# Email settings
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "mwahmeals@gmail.com")
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_RECIPIENTS = [
    "wainger25@gmail.com",
    "marcyhuang@gmail.com",
    "mylesbkeating@gmail.com",
    "marianamuneramu@gmail.com",
    "evans.abraham@gmail.com",
    "gildeah@gmail.com",
]

# Recipe selection settings
NUM_RECIPES_PER_WEEK = 3
REPEAT_WINDOW_DAYS = 45