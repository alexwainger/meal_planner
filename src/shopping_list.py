"""
Module for generating consolidated shopping lists from selected recipes.
"""

from src.utils import load_ingredients, format_ingredient


def get_recipe_ingredients(recipe_ids):
    """
    Get all ingredients for the specified recipes.
    
    Args:
        recipe_ids (list): List of recipe IDs.
        
    Returns:
        pandas.DataFrame: Ingredients for the specified recipes with recipe_index column.
    """
    ingredients_df = load_ingredients()
    recipe_ingredients = ingredients_df[ingredients_df["recipe_id"].isin(recipe_ids)].copy()
    
    # Add a recipe_index column (1-based index)
    recipe_ingredients["recipe_index"] = recipe_ingredients["recipe_id"].apply(
        lambda x: recipe_ids.index(x) + 1 if x in recipe_ids else 0
    )
    
    return recipe_ingredients


def track_recipe_sources(recipe_ingredients):
    """
    Track which recipes each ingredient comes from.
    
    Args:
        recipe_ingredients (pandas.DataFrame): Ingredients with recipe_index.
        
    Returns:
        dict: Mapping from (ingredient, unit) to list of recipe indices.
    """
    sources = {}
    for _, row in recipe_ingredients.iterrows():
        key = (row["ingredient"], row["unit"])
        if key not in sources:
            sources[key] = []
        if row["recipe_index"] not in sources[key]:
            sources[key].append(row["recipe_index"])
    
    # Sort the recipe indices
    for key in sources:
        sources[key].sort()
    
    return sources


def consolidate_ingredients(recipe_ingredients):
    """
    Consolidate ingredients with the same name and unit.
    
    Args:
        recipe_ingredients (pandas.DataFrame): Ingredients for selected recipes.
        
    Returns:
        pandas.DataFrame: Consolidated ingredients.
    """
    # Group by ingredient and unit, summing the amounts
    # Also keep the is_staple column
    grouped = recipe_ingredients.groupby(["ingredient", "unit", "is_staple"], as_index=False)["amount"].sum()
    
    # Sort by staple status (non-staples first) and then by ingredient name
    return grouped.sort_values(["is_staple", "ingredient"])


def generate_shopping_list(recipe_ids):
    """
    Generate a consolidated shopping list for the specified recipes.
    
    Args:
        recipe_ids (list): List of recipe IDs.
        
    Returns:
        dict: Dictionary with 'regular' and 'staples' lists of ingredients and recipe indices.
    """
    recipe_ingredients = get_recipe_ingredients(recipe_ids)
    
    if recipe_ingredients.empty:
        return {"regular": ["No ingredients found for the selected recipes."], "staples": []}
    
    # Track which recipes each ingredient comes from
    recipe_sources = track_recipe_sources(recipe_ingredients)
    
    consolidated = consolidate_ingredients(recipe_ingredients)
    
    # Separate the shopping list into regular items and staples
    regular_items = []
    staple_items = []
    
    for _, row in consolidated.iterrows():
        ingredient_text = row["ingredient"]
        key = (row["ingredient"], row["unit"])
        
        # Format the base ingredient text
        formatted = format_ingredient(row["amount"], row["unit"], ingredient_text)
        
        # Add the recipe indices in brackets
        if key in recipe_sources and recipe_sources[key]:
            recipe_indices = recipe_sources[key]
            formatted += f" [{', '.join(map(str, recipe_indices))}]"
        
        if row.get("is_staple", False):
            staple_items.append(formatted)
        else:
            regular_items.append(formatted)
    
    return {"regular": regular_items, "staples": staple_items}


def format_shopping_list_text(shopping_list):
    """
    Format the shopping list as a string for email or display.
    
    Args:
        shopping_list (dict): Dictionary with 'regular' and 'staples' lists.
        
    Returns:
        str: Formatted shopping list text.
    """
    result = "Shopping List:\n"
    
    # Add regular items
    if shopping_list["regular"]:
        result += "\nItems to Buy:\n"
        result += "\n".join([f"- {item}" for item in shopping_list["regular"]])
    
    # Add staple items
    if shopping_list["staples"]:
        result += "\n\nStaple Items (Check if needed):\n"
        result += "\n".join([f"- {item}" for item in shopping_list["staples"]])
    
    return result