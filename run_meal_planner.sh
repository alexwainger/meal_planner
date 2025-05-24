#!/bin/bash
# This script is scheduled to run weekly through launchd.
# To disable, run launchctl unload ~/Library/LaunchAgents/com.user.meal_planner.plist
# TO re-enable, run launchctl load ~/Library/LaunchAgents/com.user.meal_planner.plist

# Source your shell's profile to initialize conda
# This loads your regular shell configuration which should include conda
source ~/.zshrc  # Use ~/.bashrc if you're using bash instead of zsh

CONDA_ENV="meal_planner"
SCRIPT_DIR="$HOME/Projects/meal_planner"
SCRIPT="main.py"

# Activate conda environment and run script
cd "$SCRIPT_DIR" || exit 1
conda activate "$CONDA_ENV"

# Run the script
python "$SCRIPT"

# Deactivate conda environment
conda deactivate