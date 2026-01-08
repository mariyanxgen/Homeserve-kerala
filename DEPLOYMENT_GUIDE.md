# PythonAnywhere Deployment Guide

## Step 1: Create PythonAnywhere Account
1. Go to https://www.pythonanywhere.com/
2. Sign up for a free account (or paid if needed)
3. Log in to your dashboard

## Step 2: Upload Code to GitHub

### On Your Local Machine:
```bash
# 1. Create a new repository on GitHub.com (don't add README/gitignore)
# 2. Copy the repository URL (e.g., https://github.com/yourusername/homeserve-kerala.git)

# 3. Add remote and push
cd c:\entry\frontend\django_folder\homeserve
git remote add origin https://github.com/yourusername/homeserve-kerala.git
git branch -M main
git push -u origin main
```

## Step 3: Clone on PythonAnywhere

1. Open a **Bash console** on PythonAnywhere
2. Clone your repository:
```bash
git clone https://github.com/yourusername/homeserve-kerala.git
cd homeserve-kerala
```

## Step 4: Set Up Virtual Environment

```bash
# Create virtual environment with Python 3.10 (PythonAnywhere default)
mkvirtualenv --python=/usr/bin/python3.10 homeserve-venv

# Activate it
workon homeserve-venv

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Configure Django Settings

Edit `homeserve/settings.py`:

```python
# Add your PythonAnywhere domain to ALLOWED_HOSTS
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'localhost', '127.0.0.1']

# Set DEBUG to False for production
DEBUG = False

# Configure static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

## Step 6: Set Up Database

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Load sample data (optional)
python populate_all_features.py
```

## Step 7: Configure Web App

1. Go to **Web** tab on PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration** (not Django wizard)
4. Select **Python 3.10**

### Configure Source Code:
- **Source code**: `/home/yourusername/homeserve-kerala`

### Configure Virtual Environment:
- **Virtualenv**: `/home/yourusername/.virtualenvs/homeserve-venv`

### Configure WSGI File:
Click on the WSGI configuration file link and replace with:

```python
import os
import sys

# Add project directory
path = '/home/yourusername/homeserve-kerala'
if path not in sys.path:
    sys.path.append(path)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'homeserve.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Step 8: Configure Static Files

In the **Web** tab, scroll to **Static files** section:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/homeserve-kerala/staticfiles` |
| `/media/` | `/home/yourusername/homeserve-kerala/media` |

## Step 9: Reload Web App

Click the big green **Reload** button at the top of the Web tab.

## Step 10: Test Your Site

Visit: `https://yourusername.pythonanywhere.com`

## Troubleshooting

### Check Error Logs
- Go to **Web** tab
- Scroll to **Log files** section
- Check **Error log** for issues

### Common Issues

**1. Import Error**
```bash
# Make sure all packages are installed
workon homeserve-venv
pip install -r requirements.txt
```

**2. Static Files Not Loading**
```bash
python manage.py collectstatic --noinput
```
Then reload the web app.

**3. Database Errors**
```bash
python manage.py migrate
```

**4. Permission Errors**
```bash
chmod -R 755 /home/yourusername/homeserve-kerala
```

## Updating Your Site

When you make changes:

```bash
# On PythonAnywhere Bash console
cd homeserve-kerala
git pull origin main
workon homeserve-venv
pip install -r requirements.txt  # if requirements changed
python manage.py migrate  # if models changed
python manage.py collectstatic --noinput  # if static files changed
```

Then click **Reload** on the Web tab.

## Environment Variables (Optional)

Create a `.env` file on PythonAnywhere:

```bash
cd homeserve-kerala
nano .env
```

Add:
```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
```

Install python-decouple:
```bash
pip install python-decouple
```

Update settings.py:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY', default='your-fallback-key')
DEBUG = config('DEBUG', default=False, cast=bool)
```

## Database Migration to PostgreSQL (Optional)

For production with more data:

1. Sign up for free PostgreSQL at ElephantSQL or use PythonAnywhere's PostgreSQL
2. Update settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'your_db_host',
        'PORT': '5432',
    }
}
```
3. Install psycopg2: `pip install psycopg2-binary`
4. Run migrations: `python manage.py migrate`

## Security Checklist

- [ ] DEBUG = False
- [ ] SECRET_KEY changed from default
- [ ] ALLOWED_HOSTS configured
- [ ] Database credentials secured
- [ ] Admin account has strong password
- [ ] .env file not in git
- [ ] SSL/HTTPS enabled (free with PythonAnywhere)

## Free Account Limitations

- Limited to 1 web app
- Slower startup times
- Expires after 3 months (just log in to extend)
- No SSH access (use Bash console instead)
- Limited CPU time per day

For production, consider upgrading to paid account.

## Support

- PythonAnywhere Help: https://help.pythonanywhere.com/
- Forums: https://www.pythonanywhere.com/forums/
- Django Docs: https://docs.djangoproject.com/

---

Your site should now be live at: **https://yourusername.pythonanywhere.com** 🎉
