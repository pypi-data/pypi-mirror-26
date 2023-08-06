#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- notifyAll.config.settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- notifyAll settings.
"""

import os

SMS = 'sms'
EMAIL = 'email'
PUSH = 'push'

PROVIDER_APP_CLASS_PATH = 'notifyAll.providers.{0}.provider.RegisterProvider'

ALLOWED_SERVICES = (SMS, EMAIL, PUSH)

# ----------- Gmail ---------------
GMAIL_USERNAME = os.environ.get('GMAIL_USERNAME', None)
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD', None)


# # ------------ SendGrid -----------
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', None)


# # ------------ Plivo -----------
PLIVO_AUTH_ID = os.environ.get('PLIVO_AUTH_ID', None)
PLIVO_AUTH_TOKEN = os.environ.get('PLIVO_AUTH_TOKEN', None)

# # ------------ Twilio -----------
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', None)
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', None)

# # ------------- MSg91 ------------
MSG91_AUTHKEY = None
MSG91_SMS_SEND_API = 'https://control.msg91.com/api/sendhttp.php?authkey={authkey}&mobiles={mobiles}&' \
      'message={message}&sender={sender}&route={route}&country={country}'
MSG91_PROMOTIONAL_ROUTE = 1
MSG91_TRANSACTIONAL_ROUTE = 4
