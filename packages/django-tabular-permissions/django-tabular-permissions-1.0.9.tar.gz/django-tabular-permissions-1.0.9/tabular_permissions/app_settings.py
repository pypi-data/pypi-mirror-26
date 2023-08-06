from django.conf import settings
from django.utils.module_loading import import_string

TABULAR_PERMISSIONS_TEMPLATE = getattr(settings, 'TABULAR_PERMISSIONS_TEMPLATE',
                                       'tabular_permissions/admin/tabular_permissions.html')
_base_exclude_app = ['sessions', 'contenttypes', 'admin']
user_exclude = getattr(settings, 'TABULAR_PERMISSIONS_EXCLUDE', {'override': False, 'app': [], 'model': []})
if not user_exclude.get('override', False):
    TABULAR_PERMISSIONS_EXCLUDE_APPS = _base_exclude_app + user_exclude.get('app', [])
else:
    TABULAR_PERMISSIONS_EXCLUDE_APPS = user_exclude.get('app', [])
TABULAR_PERMISSIONS_EXCLUDE_APPS = [x.lower() for x in TABULAR_PERMISSIONS_EXCLUDE_APPS]

TABULAR_PERMISSIONS_EXCLUDE_MODELS = user_exclude.get('model', [])
TABULAR_PERMISSIONS_EXCLUDE_MODELS = [x.lower() for x in TABULAR_PERMISSIONS_EXCLUDE_MODELS]

TABULAR_PERMISSIONS_AUTO_IMPLEMENT = getattr(settings, 'TABULAR_PERMISSIONS_AUTO_IMPLEMENT', True)

ModelExcludeFunction = user_exclude.get('function', 'tabular_permissions.helpers.TabularPermissionDefaultExcludeFunction')
TABULAR_PERMISSIONS_EXCLUDE_FUNCTION = import_string(ModelExcludeFunction)

TABULAR_PERMISSIONS_USE_FOR_CONCRETE = getattr(settings, 'TABULAR_PERMISSIONS_USE_FOR_CONCRETE', True)
