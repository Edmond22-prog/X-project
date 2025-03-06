import os

import django
from django.utils.translation import gettext

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

django.utils.translation.ugettext = gettext
