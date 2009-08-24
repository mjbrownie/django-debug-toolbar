from debug_toolbar.panels import DebugPanel
from django.contrib.auth.models import User
#from django.template.context import get_standard_processors
from django.template.loader import render_to_string

#try:
#    from settings import DEBUG_TOOLBAR_CONFIG
#    if 'USER_GROUP_FILTER' in DEBUG_TOOLBAR_PANELS:
#

#except:
#    DEBUG_TOOLBAR_CONFIG = {}

class UserDebugPanel(DebugPanel):
    """
    A panel to show info about the current user and allow to switch user
    access.
    """

    name = 'User'
    has_content = True

    def title(self):
        return 'Users'

    def url(self):
        return ''

    def process_request(self, request):
        self.request = request

    def content(self):

        users = User.objects.all()

        context = {
            'all_users': users,
        }
        return render_to_string('debug_toolbar/panels/users.html', context)

#from django.conf import settings
from settings import DEBUG

class UserDebugPanelAuthentication:

    def authenticate(self, user_id=None):
        if not DEBUG: #TODO and not request['REMOTE_ADDR'] in INTERNAL_IPS
            return None

        return User.objects.get(pk=user_id)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

