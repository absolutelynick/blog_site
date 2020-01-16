from django.core.mail import EmailMessage
from django.core import signing
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.template import Context, Template

from urllib.parse import urlencode

from users.models import User


def send_confirm_email_link(email):
    user = get_object_or_404(User, email=email)

    token = signing.dumps(
        dict(user_uuid=user.uuid)
    )

    encrypted_token = str(urlencode(dict(token=token)))

    address = str(reverse('confirm_user_email'))

    payload = dict(
        subject = "Confirm Email",
        body = "Please confirm your email",
        email_from = "no-reply@blog.com",
        email_to = user.email,
        url = f"{address}?{encrypted_token}",
        url_name = f"{address}?{encrypted_token}",
        template = "users/password_reset_email.html",
    )

    send_email(**payload)


def send_email(subject, body, email_from, email_to, url, url_name, template):
    context = Context(
        dict(
        body = body,
        url = url,
        url_name = url_name,
        )
    )

    html_content = template.render(context)

    email_to = email_to if isinstance(email_to, list) else [email_to]

    msg = EmailMessage(subject, html_content, email_from, email_to)
    msg.content_subtype = "html"
    msg.fail_silently=False
    msg.send()