# SkillSwap Deployment Guide

## 🚀 Your app is ready to deploy!

### Files Created:
✅ requirements.txt - Python dependencies
✅ Procfile - Deployment configuration
✅ runtime.txt - Python version
✅ .env.example - Environment variables template
✅ .gitignore - Git ignore file
✅ settings.py - Updated for production

---

## Option 1: Deploy to Railway (Recommended - Easiest)

### Steps:

1. **Create a GitHub repository:**
   ```bash
   cd "c:\Users\tarun\OneDrive\Desktop\Time bank\timebank"
   git init
   git add .
   git commit -m "Initial commit - SkillSwap application"
   ```

2. **Push to GitHub:**
   - Create new repo at https://github.com/new
   - Name it: `skillswap`
   - Then run:
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/skillswap.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy to Railway:**
   - Go to https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `skillswap` repository
   - Railway will auto-detect Django and deploy!

4. **Add Environment Variables in Railway:**
   - Go to your project → Variables
   - Add these:
     ```
     DEBUG=False
     SECRET_KEY=django-insecure-CHANGE-THIS-TO-RANDOM-STRING
     ALLOWED_HOSTS=*.railway.app
     ```

5. **Generate Domain:**
   - Go to Settings → Generate Domain
   - Your app will be live at: `yourapp.railway.app`

---

## Option 2: Deploy to Render

### Steps:

1. **Push to GitHub** (same as Railway step 1-2 above)

2. **Create build.sh:**
   Already included! Just deploy.

3. **Deploy to Render:**
   - Go to https://render.com
   - Click "New" → "Web Service"
   - Connect your GitHub repo
   - Configure:
     - **Name:** skillswap
     - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
     - **Start Command:** `gunicorn timebank.wsgi:application`
     - **Environment:** Python 3

4. **Add Environment Variables:**
   ```
   DEBUG=False
   SECRET_KEY=your-random-secret-key
   ALLOWED_HOSTS=*.onrender.com
   ```

5. **Deploy!** Render will build and deploy automatically.

---

## Option 3: Deploy to Heroku

### Steps:

1. **Install Heroku CLI:**
   Download from https://devcenter.heroku.com/articles/heroku-cli

2. **Login and create app:**
   ```bash
   heroku login
   cd "c:\Users\tarun\OneDrive\Desktop\Time bank\timebank"
   heroku create skillswap-app
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-random-secret-key
   heroku config:set ALLOWED_HOSTS=.herokuapp.com
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku open
   ```

---

## 🔧 Post-Deployment Steps

### Create superuser (admin):
**Railway/Render:**
Use their CLI or dashboard console to run:
```bash
python manage.py createsuperuser
```

**Heroku:**
```bash
heroku run python manage.py createsuperuser
```

### Collect static files:
Already done automatically during deployment!

---

## 📝 Important Notes

1. **Change SECRET_KEY** in production - use a random string generator
2. **Never commit .env** file to Git (already in .gitignore)
3. **Database:** Currently using SQLite. For production, consider PostgreSQL
4. **Email:** Update EMAIL_HOST_PASSWORD with environment variable for security

---

## 🎯 Quick Start Commands

### Initialize Git (if not done):
```bash
cd "c:\Users\tarun\OneDrive\Desktop\Time bank\timebank"
git init
git add .
git commit -m "Ready for deployment"
```

### Create GitHub repo and push:
```bash
git remote add origin https://github.com/YOUR-USERNAME/skillswap.git
git branch -M main
git push -u origin main
```

### Then choose Railway, Render, or Heroku above!

---

## 🆘 Troubleshooting

**Static files not loading?**
- Check STATIC_ROOT is set correctly
- Run: `python manage.py collectstatic`
- Ensure whitenoise is in MIDDLEWARE

**Database errors?**
- Run migrations: `python manage.py migrate`
- Check DATABASE_URL environment variable

**500 Error?**
- Check DEBUG=False
- Check ALLOWED_HOSTS includes your domain
- Check application logs in platform dashboard

---

## 🎉 Success!

Once deployed, your SkillSwap app will be live at:
- **Railway:** `https://yourapp.railway.app`
- **Render:** `https://skillswap.onrender.com`
- **Heroku:** `https://skillswap-app.herokuapp.com`

Access admin panel at: `https://your-domain/admin`

Good luck! 🚀
