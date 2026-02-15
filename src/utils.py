"""
Utility functions for the meal planner application.
"""

import pandas as pd # type: ignore
from datetime import datetime


def load_recipes():
    """Load recipes from Google Sheets."""
    from src.google_sheets import get_recipes_df
    try:
        return get_recipes_df()
    except Exception as e:
        print(f"Error loading recipes from Google Sheets: {e}")
        return pd.DataFrame(columns=["recipe_id", "name", "link", "tags"])


def load_ingredients():
    """Load ingredients from Google Sheets."""
    from src.google_sheets import get_ingredients_df
    try:
        return get_ingredients_df()
    except Exception as e:
        print(f"Error loading ingredients from Google Sheets: {e}")
        return pd.DataFrame(columns=["recipe_id", "ingredient", "amount", "unit"])


def load_history():
    """Load selection history from Google Sheets."""
    from src.google_sheets import get_history_df
    try:
        return get_history_df()
    except Exception as e:
        print(f"Error loading history from Google Sheets: {e}")
        return pd.DataFrame(columns=["recipe_id", "date_selected"])


def record_selection(recipe_ids):
    """Record that recipes were selected today by appending to the history sheet."""
    from src.google_sheets import append_sheet_data
    import config

    today = datetime.now().strftime("%Y-%m-%d")
    rows = [[rid, today] for rid in recipe_ids]
    try:
        success = append_sheet_data(config.HISTORY_SHEET_NAME, rows)
        if not success:
            print("Failed to record selection to Google Sheets")
        return success
    except Exception as e:
        print(f"Error recording selection: {e}")
        return False


def format_ingredient(amount, unit, ingredient):
    """Format ingredient for display in shopping list."""
    if pd.isna(amount) or amount == 0:
        return f"{ingredient}"
    
    if pd.isna(unit) or unit.strip() == "":
        return f"{amount} {ingredient}"
    
    return f"{amount} {unit} {ingredient}"