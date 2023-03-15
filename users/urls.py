from django.urls import path

from .views import create_checkout_session, create_customer_portal_session

urlpatterns = [
    path("create-checkout-session", create_checkout_session, name="upgrade-user"),
    path(
        "create-customer-portal-session/",
        create_customer_portal_session,
        name="create-customer-portal-session",
    ),
]
