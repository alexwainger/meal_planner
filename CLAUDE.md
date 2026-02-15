# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Weekly meal planning automation: selects random recipes from a Google Sheet, generates a consolidated shopping list, emails it to recipients, and records selection history. Uses Google Sheets as the database and Gmail SMTP for delivery.

## Commands

### Local Development

A virtual environment exists at `venv/`. Always use the venv Python to run locally:

```bash
# Activate the virtual environment
source venv/bin/activate

# Set required environment variable before running
export EMAIL_PASSWORD="<gmail app-specific password>"

# Run in test mode (sends email only to wainger25@gmail.com)
python main.py --test

# Run normally (sends to all recipients)
python main.py

# Install dependencies
pip install -r requirements.txt
```

Or run directly without activating:

```bash
EMAIL_PASSWORD="<password>" venv/bin/python main.py --test
```

### Production

Scheduled via GitHub Actions (`.github/workflows/meal-plan.yml`): runs every Sunday at 9am EST. Can also be triggered manually via `workflow_dispatch`.

## Architecture

**Data flow:** Google Sheets → DataFrames → Recipe Selection → Shopping List → Email → Record History back to Sheets

Key modules in `src/`:
- **google_sheets.py** — Sheets API abstraction: auth, read/write, DataFrame conversion. All data lives in Google Sheets (no local persistence).
- **recipe_selector.py** — Selects 3 random recipes avoiding repeats within a 45-day window. Falls back to all recipes if too few are available.
- **shopping_list.py** — Fetches ingredients for selected recipes, consolidates duplicate ingredients (summing quantities), separates staples from regular items, and tracks which recipe index each ingredient belongs to.
- **email_sender.py** — Builds HTML and plaintext email with recipes and shopping list, sends via Gmail SMTP.
- **utils.py** — Lazy-loading wrappers for sheets data, `record_selection()` to append history, `format_ingredient()` for display.
- **config.py** — All configuration: sheet IDs, sheet names, recipients, `NUM_RECIPES_PER_WEEK`, `REPEAT_WINDOW_DAYS`. Secrets read from environment variables.

## Google Sheets Schema

Three sheets in one spreadsheet:
- **Recipes**: recipe_id (int), name, link (URL), tags
- **Ingredients**: recipe_id (int, FK to Recipes), ingredient, amount (float), unit, is_staple (boolean as "TRUE"/"FALSE" string)
- **History**: recipe_id (int), date_selected (YYYY-MM-DD string)

## Conventions

- Google Sheets booleans are "TRUE"/"FALSE" strings, converted to Python bools on load
- Dates stored as YYYY-MM-DD strings in sheets, converted to datetime objects in Python
- Shopping list returns structured data: each item is `{"text": "...", "sources": [1, 2]}`
- `clean_ingredient_text()` in email_sender.py removes ".0" from whole number quantities

## External Dependencies

- **Google Sheets API** via service account (`service-account-key.json`, not committed)
- **Gmail SMTP** with app-specific password

## Secrets (GitHub Actions)

Three repository secrets required: `EMAIL_PASSWORD`, `SERVICE_ACCOUNT_KEY` (full JSON), `SPREADSHEET_ID`. For local dev, set `EMAIL_PASSWORD` as an environment variable.
