"""
WSGI config for quora project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

#import os
#
#from django.core.wsgi import get_wsgi_application
#
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quora.settings')
#
#application = get_wsgi_application()
"""
    WSGI config for interface24 project.

    It exposes the WSGI callable as a module-level variable named ``application``.

    For more information on this file, see
    https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
    """
import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/angara/interface/')
sys.path.append('/home/angara/interface/interface24')
sys.path.append('/home/angara/interface/interface24/quora')
sys.path.append('/home/angara/interface/venv/lib/python3.7/site-packages')
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quora.settings')

application = get_wsgi_application()
