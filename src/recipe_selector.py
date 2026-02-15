"""
Module for selecting recipes based on history and preferences.
"""

from datetime import datetime, timedelta
import config
from src.utils import load_recipes, load_history


def select_recipes():
    """
    Select recipes for the week, avoiding recipes used within the repeat window.
    
    Returns:
        list: List of selected recipe dictionaries with id, name, and link.
    """
    recipes_df = load_recipes()
    history_df = load_history()
    
    if recipes_df.empty:
        raise ValueError("No recipes available. Please add recipes first.")
    
    # Calculate the cutoff date for the repeat window
    cutoff_date = datetime.now() - timedelta(days=config.REPEAT_WINDOW_DAYS)
    
    # Get recipe IDs that were recently used (within repeat window)
    if not history_df.empty and "date_selected" in history_df.columns:
        recent_recipe_ids = history_df[history_df["date_selected"] > cutoff_date]["recipe_id"].unique()
    else:
        recent_recipe_ids = []
    
    # Filter out recently used recipes
    available_recipes = recipes_df[~recipes_df["recipe_id"].isin(recent_recipe_ids)]
    
    if len(available_recipes) < config.NUM_RECIPES_PER_WEEK:
        print(f"Warning: Only {len(available_recipes)} recipes available within the repeat window. "
              f"Some recipes might be repeated sooner than expected.")
        # Fall back to using all recipes if we don't have enough
        available_recipes = recipes_df
    
    # Select random recipes
    selected_recipes = available_recipes.sample(min(config.NUM_RECIPES_PER_WEEK, len(available_recipes)))
    
    # Format the selected recipes as a list of dictionaries
    result = []
    for _, recipe in selected_recipes.iterrows():
        result.append({
            "id": recipe["recipe_id"],
            "name": recipe["name"],
            "link": recipe["link"]
        })
    
    return result