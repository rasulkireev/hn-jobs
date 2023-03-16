import math
from django.forms.utils import ErrorList
from django.db.utils import IntegrityError
import logging

from allauth.account.models import EmailAddress
from djstripe.models import Customer, Subscription

logger = logging.getLogger(__file__)


def add_users_context(context, user):
    try:
        customer = Customer.objects.get(subscriber=user)
        logger.info(f"Adding customer {customer} to context (id: {customer.id}).")
        context["customer"] = customer

        try:
            subscription = Subscription.objects.get(customer=customer)
            logger.info(f"Adding subscription {subscription} to context.")
            context["subscription"] = subscription
        except Subscription.DoesNotExist as e:
            logger.error(f"Subscription Error: {e}")

    except (Customer.DoesNotExist, IntegrityError) as e:
        logger.error(f"Customer Error: {e}")
        customer = Customer.create(subscriber=user)
        logging.info(f"Created User: {customer}")

    try:
        context["email_verified"] = EmailAddress.objects.get_for_user(user, user.email).verified
    except EmailAddress.DoesNotExist as e:
        logger.error(f"Email Error: {e}")

    return context


def floor_to_thousands(x):
    return int(math.floor(x / 1000.0)) * 1000

def floor_to_tens(x):
    return int(math.floor(x / 10.0)) * 10

class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return f"""
            <div class="p-4 my-4 border border-red-600 border-solid rounded-md bg-red-50">
              <div class="flex">
                <div class="flex-shrink-0">
                  <!-- Heroicon name: solid/x-circle -->
                  <svg class="w-5 h-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3 text-sm text-red-700">
                      {''.join(['<p>%s</p>' % e for e in self])}
                </div>
              </div>
            </div>
         """