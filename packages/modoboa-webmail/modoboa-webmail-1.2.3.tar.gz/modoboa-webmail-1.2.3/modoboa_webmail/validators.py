"""Custom form validators."""

from email.utils import getaddresses

from django.utils.encoding import force_text
from django.core.validators import validate_email


class EmailListValidator(object):

    """Validate a semi-comma separated list of email."""

    def __call__(self, value):
        value = force_text(value)
        emails = [email.strip() for email in value.split(";")]
        addresses = getaddresses(emails)
        [validate_email(email) for name, email in addresses]


validate_email_list = EmailListValidator()
