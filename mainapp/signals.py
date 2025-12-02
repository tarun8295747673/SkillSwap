from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(user_logged_in)
def send_login_email(sender, request, user, **kwargs):
    subject = 'Login Alert - TimeBank'
    message = f'Hi {user.username},\n\nYou have successfully logged in to your TimeBank account.'
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        email = user.userprofile.email   # ✅ Get email from UserProfile
    except:
        email = None

    if email:  # ✅ Only if email exists
        send_mail(subject, message, from_email, [email])
