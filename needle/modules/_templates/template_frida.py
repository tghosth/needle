from __future__ import unicode_literals
from core.framework.module import FridaModule


class Module(FridaModule):
    meta = {
        'name': 'Title',
        'author': '@AUTHOR (@TWITTER)',
        'description': 'Description',
        'options': (
        ),
    }

    # ==================================================================================================================
    # UTILS
    # ==================================================================================================================

    # ==================================================================================================================
    # RUN
    # ==================================================================================================================
    def module_run(self):
        pass
