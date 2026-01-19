#!/bin/bash

# Quick deployment script for PythonAnywhere

echo "🚀 HomeServe Kerala - PythonAnywhere Deployment"
echo "================================================"
echo ""

# Step 1: Setup virtual environment
echo "📦 Setting up virtual environment..."
mkvirtualenv --python=/usr/bin/python3.10 homeserve-venv
workon homeserve-venv

# Step 2: Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Step 3: Database setup
echo "🗄️  Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Step 4: Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Step 5: Create superuser
echo "👤 Create superuser account:"
python manage.py createsuperuser

# Step 6: Load sample data (optional)
read -p "Load sample data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "📊 Loading sample data..."
    python populate_all_features.py
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure WSGI file in PythonAnywhere Web tab"
echo "2. Set static files mappings"
echo "3. Reload your web app"
echo ""
echo "See DEPLOYMENT_GUIDE.md for detailed instructions"
