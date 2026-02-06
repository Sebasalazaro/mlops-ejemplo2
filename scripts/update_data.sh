#!/bin/bash
# Push updated parking data to GitHub repository

set -e  # Exit on error

# Configure git user
git config --global user.name 'github-actions[bot]'
git config --global user.email 'github-actions[bot]@users.noreply.github.com'

# Stage all changes
git add .

# Check if there are changes to commit
if git status | grep -q modified; then
    echo "Changes detected, committing and pushing..."
    git commit -am "chore: update parking availability data"
    git push
else
    echo "No changes since last run"
fi
