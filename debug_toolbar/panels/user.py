from debug_toolbar.panels import DebugPanel
from django.contrib.auth.models import User, Group
#from django.template.context import get_standard_processors
from django.template.loader import render_to_string

def get_debug_users():
    """
    Returns a list if context switchable users based on the criteria outlined
    in settings
    """
    users = User.objects.all()

    try:
        from settings import DEBUG_TOOLBAR_CONFIG
        if 'USER_EXCLUDE' in DEBUG_TOOLBAR_CONFIG:
            users = users.exclude(**DEBUG_TOOLBAR_CONFIG['USER_EXCLUDE'])
        if 'USER_INCLUDE' in DEBUG_TOOLBAR_CONFIG:
            users = users.filter(**DEBUG_TOOLBAR_CONFIG['USER_INCLUDE'])
    except:
        pass
        
    return users

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



        groups = Group.objects.all()
        context = {
                'groups': groups,
                'active_user': self.request.user,
                'all_users': get_debug_users(),
        }
        return render_to_string('debug_toolbar/panels/users.html', context)

    def get_custom_permissions(self):

        from django.contrib.contenttypes.models import ContentType
#        from django.contrib.auth.models import Permission
        from django.db.models import get_models

        permissions = []

        for klass in get_models():
            if klass._meta.permissions:
                ctype = ContentType.objects.get_for_model(klass)
                permissions.append((ctype, klass._meta.permissions ))

        return permissions
#from django.conf import settings
from settings import DEBUG

class UserDebugPanelAuthentication:

    """
    This authentication module will accept any login so long as the
    settings.DEBUG variable is set to True.
    """
    def authenticate(self, user_id=None):
        try:
            from settings import DEBUG_TOOLBAR_PANELS
        except:
            return None

        if not DEBUG \
            or not 'debug_toolbar.panels.user.UserDebugPanel' \
            in DEBUG_TOOLBAR_PANELS:
            assert False
            return None

        return User.objects.get(pk=user_id)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

