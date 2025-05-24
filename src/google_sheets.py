"""
Module for interacting with Google Sheets API using a service account.
"""

import pandas as pd # type: ignore
from googleapiclient.discovery import build # type: ignore
from google.oauth2 import service_account # type: ignore

import config

# Define the scopes - updated to include write access
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_google_sheets_service():
    """
    Get authenticated Google Sheets service using a service account.
    
    Returns:
        googleapiclient.discovery.Resource: Authorized Google Sheets API service.
    """
    try:
        # Use service account credentials from the specified file
        credentials = service_account.Credentials.from_service_account_file(
            config.SERVICE_ACCOUNT_FILE, 
            scopes=SCOPES
        )
        
        # Build and return the service
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except Exception as e:
        print(f"Error setting up Google Sheets service: {e}")
        raise


def get_sheet_data(sheet_name):
    """
    Get data from a specific sheet in the configured Google Spreadsheet.
    
    Args:
        sheet_name (str): Name of the sheet to read.
        
    Returns:
        list: List of rows from the sheet.
    """
    try:
        service = get_google_sheets_service()
        sheet = service.spreadsheets()
        
        # Get the sheet data
        result = sheet.values().get(
            spreadsheetId=config.SPREADSHEET_ID,
            range=f"{sheet_name}"
        ).execute()
        
        values = result.get('values', [])
        if not values:
            print(f"No data found in sheet '{sheet_name}'")
            return []
            
        return values
        
    except Exception as e:
        print(f"Error accessing Google Sheets: {e}")
        return []


def update_sheet_data(sheet_name, values):
    """
    Update data in a specific sheet in the configured Google Spreadsheet.
    
    Args:
        sheet_name (str): Name of the sheet to update.
        values (list): List of rows to write to the sheet.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        service = get_google_sheets_service()
        sheet = service.spreadsheets()
        
        # Clear the sheet first
        sheet.values().clear(
            spreadsheetId=config.SPREADSHEET_ID,
            range=f"{sheet_name}"
        ).execute()
        
        # Update the sheet with new data
        sheet.values().update(
            spreadsheetId=config.SPREADSHEET_ID,
            range=f"{sheet_name}!A1",
            valueInputOption='RAW',
            body={'values': values}
        ).execute()
        
        return True
        
    except Exception as e:
        print(f"Error updating Google Sheets: {e}")
        return False


def append_sheet_data(sheet_name, values):
    """
    Append data to a specific sheet in the configured Google Spreadsheet.
    
    Args:
        sheet_name (str): Name of the sheet to append to.
        values (list): List of rows to append to the sheet.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        service = get_google_sheets_service()
        sheet = service.spreadsheets()
        
        # Append the data
        sheet.values().append(
            spreadsheetId=config.SPREADSHEET_ID,
            range=f"{sheet_name}",
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': values}
        ).execute()
        
        return True
        
    except Exception as e:
        print(f"Error appending to Google Sheets: {e}")
        return False


def sheet_to_dataframe(sheet_name, dtypes):
    """
    Convert Google Sheet data to a pandas DataFrame.
    
    Args:
        sheet_name (str): Name of the sheet to read.
        dtypes (dict): Dictionary of column names and their data types.

    Returns:
        pandas.DataFrame: DataFrame containing the sheet data.
    """
    values = get_sheet_data(sheet_name)
    
    if not values:
        return pd.DataFrame()  # Return empty DataFrame
    
    # First row is headers
    headers = values[0]
    
    # Rest are data rows
    data = values[1:]
    
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=headers)
    
    # Apply data types where column exists
    for col, dtype in dtypes.items():
        if col in df.columns:
            if dtype == 'datetime':
                df[col] = pd.to_datetime(df[col], format="%Y-%m-%d")
            else:
                df[col] = df[col].astype(dtype)
    
    return df


def dataframe_to_sheet(sheet_name, df):
    """
    Write a pandas DataFrame to a Google Sheet.
    
    Args:
        sheet_name (str): Name of the sheet to write to.
        df (pandas.DataFrame): DataFrame to write.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    if df.empty:
        # If DataFrame is empty, just write headers
        headers = df.columns.tolist()
        values = [headers]
    else:
        # Convert DataFrame to list of lists
        # Handle datetime formatting
        df_copy = df.copy()
        for col in df_copy.columns:
            if pd.api.types.is_datetime64_any_dtype(df_copy[col]):
                df_copy[col] = df_copy[col].dt.strftime('%Y-%m-%d')
        
        headers = df_copy.columns.tolist()
        data = df_copy.values.tolist()
        values = [headers] + data
    
    return update_sheet_data(sheet_name, values)


def get_recipes_df():
    """
    Get recipes from Google Sheets as a DataFrame.
    
    Returns:
        pandas.DataFrame: DataFrame of recipes.
    """
    recipes_df = sheet_to_dataframe(config.RECIPES_SHEET_NAME, dtypes={'recipe_id': 'int'})
    
    # Make sure required columns exist
    required_cols = ["recipe_id", "name", "link", "tags"]
    for col in required_cols:
        if col not in recipes_df.columns:
            print(f"Warning: Recipe sheet missing required column '{col}'")
            recipes_df[col] = ""
            
    return recipes_df


def get_ingredients_df():
    """
    Get ingredients from Google Sheets as a DataFrame.
    
    Returns:
        pandas.DataFrame: DataFrame of ingredients.
    """
    ingredients_df = sheet_to_dataframe(
        config.INGREDIENTS_SHEET_NAME,
        dtypes={'recipe_id': 'int', 'amount': 'float'}
    )
    
    # Make sure required columns exist
    required_cols = ["recipe_id", "ingredient", "amount", "unit", "is_staple"]
    for col in required_cols:
        if col not in ingredients_df.columns:
            print(f"Warning: Ingredients sheet missing required column '{col}'")
            ingredients_df[col] = ""
    
    # Convert is_staple column to boolean
    val_map = {'TRUE': True, 'FALSE': False}
    if "is_staple" in ingredients_df.columns:
        ingredients_df["is_staple"] = ingredients_df["is_staple"].map(val_map)

    return ingredients_df


def get_history_df():
    """
    Get history from Google Sheets as a DataFrame.
    
    Returns:
        pandas.DataFrame: DataFrame of history.
    """
    history_df = sheet_to_dataframe(
        config.HISTORY_SHEET_NAME,
        dtypes={'recipe_id': 'int', 'date_selected': 'datetime'}
    )
    
    # Make sure required columns exist
    required_cols = ["recipe_id", "date_selected"]
    for col in required_cols:
        if col not in history_df.columns:
            print(f"Warning: History sheet missing required column '{col}'")
            if col == "recipe_id":
                history_df[col] = 0
            elif col == "date_selected":
                history_df[col] = pd.to_datetime('1900-01-01')
    
    return history_df


def save_history_df(history_df):
    """
    Save history DataFrame to Google Sheets.
    
    Args:
        history_df (pandas.DataFrame): DataFrame of history to save.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    return dataframe_to_sheet(config.HISTORY_SHEET_NAME, history_df)