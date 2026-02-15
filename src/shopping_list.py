"""
Module for generating consolidated shopping lists from selected recipes.
"""

from src.utils import load_ingredients, format_ingredient


def get_recipe_ingredients(recipe_ids):
    """
    Get all ingredients for the specified recipes.

    Returns:
        pandas.DataFrame: Ingredients for the specified recipes with recipe_index column.
    """
    ingredients_df = load_ingredients()
    recipe_ingredients = ingredients_df[ingredients_df["recipe_id"].isin(recipe_ids)].copy()

    recipe_ingredients["recipe_index"] = recipe_ingredients["recipe_id"].apply(
        lambda x: recipe_ids.index(x) + 1 if x in recipe_ids else 0
    )

    return recipe_ingredients


def track_recipe_sources(recipe_ingredients):
    """
    Track which recipes each ingredient comes from.

    Returns:
        dict: Mapping from (ingredient, unit) to sorted list of recipe indices.
    """
    sources = {}
    for _, row in recipe_ingredients.iterrows():
        key = (row["ingredient"], row["unit"])
        if key not in sources:
            sources[key] = []
        if row["recipe_index"] not in sources[key]:
            sources[key].append(row["recipe_index"])

    for key in sources:
        sources[key].sort()

    return sources


def consolidate_ingredients(recipe_ingredients):
    """Consolidate ingredients with the same name and unit, summing amounts."""
    grouped = recipe_ingredients.groupby(["ingredient", "unit", "is_staple"], as_index=False)["amount"].sum()
    return grouped.sort_values(["is_staple", "ingredient"])


def generate_shopping_list(recipe_ids):
    """
    Generate a consolidated shopping list for the specified recipes.

    Returns:
        dict with 'regular' and 'staples' lists. Each item is a dict with:
            - text: formatted ingredient string
            - sources: list of 1-based recipe indices
    """
    recipe_ingredients = get_recipe_ingredients(recipe_ids)

    if recipe_ingredients.empty:
        return {"regular": [], "staples": []}

    recipe_sources = track_recipe_sources(recipe_ingredients)
    consolidated = consolidate_ingredients(recipe_ingredients)

    regular_items = []
    staple_items = []

    for _, row in consolidated.iterrows():
        key = (row["ingredient"], row["unit"])
        item = {
            "text": format_ingredient(row["amount"], row["unit"], row["ingredient"]),
            "sources": recipe_sources.get(key, []),
        }

        if row.get("is_staple", False):
            staple_items.append(item)
        else:
            regular_items.append(item)

    return {"regular": regular_items, "staples": staple_items}