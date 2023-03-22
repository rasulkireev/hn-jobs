import logging
import stripe

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView

from djstripe import models, webhooks, settings as djstripe_settings
from allauth.account.utils import send_email_confirmation

from .models import CustomUser
from hn_jobs.utils import add_users_context

stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__file__)

class UserSettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "account_login"
    model = CustomUser
    fields = ["name"]
    success_message = "User Profile Updated"
    success_url = reverse_lazy("settings")
    template_name = "account/settings.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        add_users_context(context, user)

        return context

def create_checkout_session(request):
    user = request.user
    price_id = models.Price.objects.all().first().id

    customer = models.Customer.objects.get(subscriber=user)

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "quantity": 1,
                "price": price_id,
            }
        ],
        mode="subscription",
        success_url=request.build_absolute_uri(reverse_lazy("profiles")) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse_lazy("home")) + "?status=failed",
        customer=customer.id,
        metadata={"price_id": price_id},
        allow_promotion_codes=True,
        automatic_tax={"enabled": True},
        customer_update={
            "address": "auto",
        },
        payment_method_types=["card"],
    )

    return redirect(checkout_session.url, code=303)

@webhooks.handler("checkout.session.completed")
def successfull_payment_webhook(event, **kwargs):
    if event.type == "checkout.session.completed":
        customer = event.data["object"]["customer"]
        logger.info(f"Upgrading Customer: {customer}")
        models.Customer.sync_from_stripe_data(stripe.Customer.retrieve(customer))

    return HttpResponse(status=200)


def create_customer_portal_session(request):
    customer = models.Customer.objects.get(subscriber=request.user)
    session = stripe.billing_portal.Session.create(
        customer=customer.id,
        return_url=request.build_absolute_uri(reverse_lazy("home")),
    )

    return redirect(session.url)

def resend_email_confirmation_email(request):
    user = request.user
    send_email_confirmation(request, user, user.email)

    return redirect("settings")
