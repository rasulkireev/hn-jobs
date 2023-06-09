from django.urls import path

from .views import (
    UserSettingsView,
    create_checkout_session,
    create_customer_portal_session,
    resend_email_confirmation_email,
)

urlpatterns = [
    path("settings/", UserSettingsView.as_view(), name="settings"),
    path("create-checkout-session", create_checkout_session, name="upgrade-user"),
    path(
        "create-customer-portal-session/",
        create_customer_portal_session,
        name="create-customer-portal-session",
    ),
    path(
        "send-confirmation",
        resend_email_confirmation_email,
        name="resend_email_confirmation_email",
    ),
]
