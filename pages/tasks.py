import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__file__)


def send_confirmation_email(instance, confirmation_url):
    message = f"""
      Hey there,

      Thanks a ton for the alert subscription for {instance["technology_selected"]} jobs.

      To make sure you start receving weekly alerts,
      please confirm your subscription by clicking the link below:

      {confirmation_url}
    """
    send_mail(
        "Confirm Your Job Alert Subscription",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [instance["email"]],
        fail_silently=False,
    )


def email_support_request(instance):
    message = f"""
      User: {instance['current_user'].username}
      User Email: {instance['current_user'].email}
      Message: {instance['message']}.
    """
    send_mail(
        f"Support Request from {instance['current_user'].username}",
        message,
        "rasul@builtwithdjango.com",
        ["rasul@builtwithdjango.com"],
        fail_silently=False,
    )
