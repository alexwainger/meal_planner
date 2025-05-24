"""
Main script for the meal planning application.
"""

import argparse
from datetime import datetime

import config
from src.utils import record_selection #, ensure_directories_exist
from src.recipe_selector import select_recipes
from src.shopping_list import generate_shopping_list
from src.email_sender import send_email


def generate_weekly_plan(test_mode=False):
    """
    Generate the weekly meal plan and shopping list, and send via email.
    
    Args:
        test_mode (bool): If True, only send email to the first recipient for testing.
    """
    print(f"Generating meal plan for week of {datetime.now().strftime('%Y-%m-%d')}...")
    if test_mode:
        print("Running in TEST MODE - email will only be sent to wainger25@gmail.com")
    
    # Select recipes
    try:
        selected_recipes = select_recipes()
        recipe_ids = [recipe["id"] for recipe in selected_recipes]
        
        # Generate shopping list
        shopping_list = generate_shopping_list(recipe_ids)
        
        # Print the selected recipes and shopping list
        print("\nSelected Recipes:")
        for recipe in selected_recipes:
            print(f"- {recipe['name']} ({recipe['link']})")
        
        # Send email
        if config.EMAIL_SENDER and config.EMAIL_RECIPIENTS:
            send_success = send_email(selected_recipes, shopping_list, test_mode=test_mode)
            if send_success:
                # Record the selections in history
                record_selection(recipe_ids)
                if test_mode:
                    print("Test meal plan generated and sent successfully!")
                else:
                    print("Meal plan generated and sent successfully!")
            else:
                print("Failed to send email. Check your email settings.")
        else:
            # Record the selections in history even if no email is sent
            record_selection(recipe_ids)
            print("Email sending is not configured. Add email settings to config.py to enable.")
            print("Meal plan generated successfully!")
        
        return True
        
    except Exception as e:
        print(f"Error generating meal plan: {e}")
        return False


def main():
    """
    Main function to run the meal planning assistant.
    """
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Meal Planning Assistant')
    # parser.add_argument('--plan', action='store_true', 
    #                    help='Generate and send weekly meal plan')
    parser.add_argument('--test', action='store_true',
                       help='Test mode - only send email to wainger25@gmail.com')
    
    args = parser.parse_args()
    
    # Ensure all directories and files exist
    # ensure_directories_exist()

    # If --plan flag is provided, run the meal plan generation
    # if args.plan:
        # generate_weekly_plan(test_mode=args.test)
    # else:
    # Default behavior - run meal plan generation
    generate_weekly_plan(test_mode=args.test)
    
if __name__ == "__main__":
    main()