# SkillSwap - Render Deployment Guide

## 🚀 Deploy to Render

Your SkillSwap application is configured and ready to deploy to Render!

---

## Step-by-Step Deployment:

### 1. **Create GitHub Repository**

First, push your code to GitHub:

```bash
# Create a new repository at https://github.com/new
# Name it: skillswap
# Make it Public
# Don't initialize with README

# Then run these commands:
git remote add origin https://github.com/YOUR-USERNAME/skillswap.git
git branch -M main
git push -u origin main
```

---

### 2. **Sign Up for Render**

- Go to https://render.com
- Click "**Get Started**"
- Sign up with your **GitHub account** (recommended)

---

### 3. **Create New Web Service**

1. Click "**New +**" button (top right)
2. Select "**Web Service**"
3. Click "**Connect account**" to authorize GitHub
4. Find and select your `skillswap` repository
5. Click "**Connect**"

---

### 4. **Configure Your Service**

Fill in these settings:

- **Name:** `skillswap` (or your preferred name)
- **Region:** Choose closest to you
- **Branch:** `main`
- **Runtime:** `Python 3`
- **Build Command:**
  ```
  ./build.sh
  ```
- **Start Command:**
  ```
  gunicorn timebank.wsgi:application
  ```

---

### 5. **Add Environment Variables**

Scroll down to "**Environment Variables**" section and add these:

Click "**Add Environment Variable**" for each:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | `django-skillswap-secret-key-change-this-to-random-string` |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `PYTHON_VERSION` | `3.13.0` |

**Important:** Change the SECRET_KEY to a random string for security!

---

### 6. **Select Plan**

- Choose "**Free**" plan (suitable for testing)
- Click "**Create Web Service**"

---

### 7. **Wait for Deployment**

Render will now:
1. ✅ Clone your repository
2. ✅ Run `build.sh` (install dependencies, collect static files, migrate database)
3. ✅ Start your application with gunicorn
4. ✅ Assign a URL

This takes **5-10 minutes** for the first deployment.

---

### 8. **View Your Live App**

Once deployment is complete (green checkmark):

- Your app will be live at: `https://skillswap.onrender.com`
- Or your custom name: `https://your-app-name.onrender.com`

Click the URL at the top to open your live SkillSwap application! 🎉

---

## 🔧 Post-Deployment Steps

### Create Superuser (Admin Account)

1. In your Render dashboard, go to your service
2. Click "**Shell**" tab (left sidebar)
3. Click "**Launch Shell**"
4. Run this command:
   ```bash
   python manage.py createsuperuser
   ```
5. Enter username, email, and password when prompted

Now you can access admin panel at: `https://your-app.onrender.com/admin`

---

## 🎨 Static Files

Static files (CSS, JS, images) are automatically collected and served by Whitenoise during the build process. No extra configuration needed!

---

## 🔄 Future Updates

When you make changes to your app:

```bash
# Make your changes, then:
git add .
git commit -m "Describe your changes"
git push origin main
```

Render will automatically detect the push and redeploy your app!

---

## 📊 Monitor Your App

In Render dashboard:
- **Logs:** View real-time application logs
- **Metrics:** See CPU and memory usage
- **Events:** Track deployments and system events
- **Shell:** Access command-line interface

---

## 🆘 Troubleshooting

### App won't start?
- Check "**Logs**" tab for errors
- Verify environment variables are set correctly
- Ensure `build.sh` has correct permissions

### Static files not loading?
- Check build logs for `collectstatic` completion
- Verify `STATIC_ROOT` in settings.py
- Ensure Whitenoise is in MIDDLEWARE

### Database errors?
- Render provides a free PostgreSQL database if needed
- Current setup uses SQLite (file-based)
- For production, consider upgrading to PostgreSQL

### Custom Domain?
- Go to Settings → Custom Domain
- Add your domain and follow DNS instructions
- Free tier supports custom domains!

---

## 🎉 Success Checklist

- ✅ Code pushed to GitHub
- ✅ Render account created
- ✅ Web service configured
- ✅ Environment variables added
- ✅ App deployed successfully
- ✅ Admin account created
- ✅ App accessible via URL

**Your SkillSwap app is now LIVE!** 🚀

Access it at: `https://your-app-name.onrender.com`

---

## 💡 Pro Tips

1. **Keep your SECRET_KEY secret** - Never commit it to Git
2. **Monitor logs** regularly for errors
3. **Set up alerts** in Render for downtime notifications
4. **Upgrade to paid plan** for:
   - No cold starts (instant loading)
   - Continuous deployment
   - More resources
   - Better uptime

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
- Render Community: https://community.render.com/

Good luck with your deployment! 🎊
