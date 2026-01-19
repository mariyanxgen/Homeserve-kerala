#!/bin/bash

# Update script for PythonAnywhere deployment
# Run this script in your PythonAnywhere Bash console

echo "🚀 Updating HomeServe Kerala on PythonAnywhere"
echo "==============================================="
echo ""

# Navigate to project directory
cd ~/homeserve-kerala

# Step 1: Pull latest changes
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Step 2: Activate virtual environment
echo "🔧 Activating virtual environment..."
workon homeserve-venv

# Step 3: Update dependencies (if needed)
echo "📦 Updating dependencies..."
pip install -r requirements.txt

# Step 4: Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Step 5: Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Step 6: Restart web app
echo "🔄 Restarting web app..."
echo "   ⚠️  Go to the Web tab and click the green 'Reload' button"
echo ""

echo "✅ Update complete!"
echo ""
echo "Don't forget to:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Click the 'Reload yourusername.pythonanywhere.com' button"
echo "3. Check your site at https://yourusername.pythonanywhere.com"
echo "4. Check error logs if something doesn't work"
echo ""
