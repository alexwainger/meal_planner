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
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=["recipe_id", "name", "link", "tags"])


def load_ingredients():
    """Load ingredients from Google Sheets."""
    from src.google_sheets import get_ingredients_df
    try:
        return get_ingredients_df()
    except Exception as e:
        print(f"Error loading ingredients from Google Sheets: {e}")
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=["recipe_id", "ingredient", "amount", "unit"])


def load_history():
    """Load selection history from Google Sheets."""
    from src.google_sheets import get_history_df
    try:
        return get_history_df()
    except Exception as e:
        print(f"Error loading history from Google Sheets: {e}")
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=["recipe_id", "date_selected"])


def save_history(history_df):
    """Save selection history to Google Sheets."""
    from src.google_sheets import save_history_df
    try:
        success = save_history_df(history_df)
        if not success:
            print("Failed to save history to Google Sheets")
        return success
    except Exception as e:
        print(f"Error saving history to Google Sheets: {e}")
        return False


def record_selection(recipe_ids):
    """Record that recipes were selected today."""
    history_df = load_history()
    today = datetime.now()
    
    new_records = pd.DataFrame({
        "recipe_id": recipe_ids,
        "date_selected": [today] * len(recipe_ids)
    })
    
    updated_history = pd.concat([history_df, new_records], ignore_index=True)
    return save_history(updated_history)


def format_ingredient(amount, unit, ingredient):
    """Format ingredient for display in shopping list."""
    if pd.isna(amount) or amount == 0:
        return f"{ingredient}"
    
    if pd.isna(unit) or unit.strip() == "":
        return f"{amount} {ingredient}"
    
    return f"{amount} {unit} {ingredient}"