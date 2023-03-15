import logging
import stripe

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse

from djstripe import models, webhooks, settings as djstripe_settings

stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__file__)

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