import sys

import django
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

import debug_toolbar
from debug_toolbar.panels import DebugPanel


class ViewFunctionDebugPanel(DebugPanel):
    """
    Panel that displays the Django version.
    """
    name = 'View Function'
    has_content = True

    def nav_title(self):
        return _('View Function')

    def nav_subtitle(self):
        return ''

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.view_func = view_func

    def url(self):
        return ''

    def title(self):
        return _('View Function')

    def content(self):
        import inspect

        try:
            func_source = inspect.getsource(self.view_func)
        except:
            func_source = '< inspect.getsource has failed >'

        #decorator
        try:
            view = inspect.getsource ( self.view_func.view_func )
        except:
            view = ''

        render =  render_to_string('debug_toolbar/panels/view_func.html', {
            'view_func': self.view_func.func_name ,
            'func_file': self.view_func.func_code.co_filename,
            'func_source':func_source,
            'view': view
            } 
            )
        
        return render
