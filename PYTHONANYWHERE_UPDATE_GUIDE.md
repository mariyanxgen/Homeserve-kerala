# Quick PythonAnywhere Update Steps

## 🚀 Your changes have been pushed to GitHub!

Follow these steps to deploy to PythonAnywhere:

## Option 1: Using the Update Script (Recommended)

### 1. Open PythonAnywhere Bash Console
- Go to https://www.pythonanywhere.com
- Log in to your account
- Click on **"Bash"** under "New console" or use an existing console

### 2. Run the Update Script
```bash
cd ~/homeserve-kerala
bash update_pythonanywhere.sh
```

### 3. Reload Your Web App
- Go to the **Web** tab in PythonAnywhere dashboard
- Click the big green **"Reload yourusername.pythonanywhere.com"** button

### 4. Test Your Changes
Visit: `https://yourusername.pythonanywhere.com`

---

## Option 2: Manual Update Steps

If you prefer to run commands manually:

### 1. Open PythonAnywhere Bash Console

### 2. Navigate to Your Project
```bash
cd ~/homeserve-kerala
```

### 3. Pull Latest Changes
```bash
git pull origin main
```

### 4. Activate Virtual Environment
```bash
workon homeserve-venv
```

### 5. Install/Update Dependencies
```bash
pip install -r requirements.txt
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Reload Web App
- Go to the **Web** tab
- Click **"Reload yourusername.pythonanywhere.com"**

---

## ✅ What Was Updated

The following changes were deployed:
- **Provider CRUD Operations**: Full create, read, update, delete functionality
- **Delete Confirmation**: Added confirmation page before deleting services
- **Provider Dashboard**: Updated service management interface
- **Documentation**: Added implementation and testing guides

---

## 🧪 Testing Provider CRUD on PythonAnywhere

### Login as Provider
- URL: `https://yourusername.pythonanywhere.com/login/`
- Username: `provider1`
- Password: `password123`

### Test Service Management
1. **View Services**: `https://yourusername.pythonanywhere.com/provider/services/`
2. **Add Service**: Click "Add New Service" button
3. **Edit Service**: Click "Edit" on any service
4. **Delete Service**: Click "Delete" and confirm

---

## 🐛 Troubleshooting

### Check Error Logs
If something doesn't work:
1. Go to **Web** tab
2. Scroll to **Log files** section
3. Click on **Error log**

### Common Issues

**Static Files Not Loading**
```bash
cd ~/homeserve-kerala
workon homeserve-venv
python manage.py collectstatic --noinput
```
Then reload the web app.

**Database Errors**
```bash
python manage.py migrate
```

**Import Errors**
```bash
workon homeserve-venv
pip install -r requirements.txt
```

---

## 📊 Database Status

**Local Database**: Already migrated ✅
**PythonAnywhere Database**: Will be migrated when you run the update script

---

## 🔄 Future Updates

Whenever you make changes locally:

1. **Commit & Push**:
```bash
git add -A
git commit -m "Your commit message"
git push origin main
```

2. **Update PythonAnywhere**:
```bash
# In PythonAnywhere Bash console
cd ~/homeserve-kerala
bash update_pythonanywhere.sh
```

3. **Reload Web App** (in Web tab)

---

## 📝 Notes

- The update script (`update_pythonanywhere.sh`) has been created and pushed to GitHub
- No database changes were detected (no new migrations needed)
- All your provider CRUD features are ready to deploy
- Remember to reload the web app after running the update script!

---

## 🎉 Your Site

Once deployed, your HomeServe Kerala site will be live at:
**https://yourusername.pythonanywhere.com**

Provider dashboard will be at:
**https://yourusername.pythonanywhere.com/provider/services/**

---

Need help? Check the error logs or the DEPLOYMENT_GUIDE.md file!
