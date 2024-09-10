import os
# For sending email
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
#For link genarate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def get_upload_to(instance, filename):
    return os.path.join('accounts/images/', filename)

def generate_confirmation_link(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    confirm_link = f"http://127.0.0.1:9000/user/activate/?uid64={uid}&token={token}"
    
    return confirm_link

def send_email(user, subject, template, extra=None):
    email_subject = subject
    email_body = render_to_string(template, {
        'extra' : extra,
        'user': user,
        'current_year': timezone.now().year,
    })
    email = EmailMultiAlternatives(email_subject, '', to=[user.email])
    email.attach_alternative(email_body, "text/html")
    email.send()

