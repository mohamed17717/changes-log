## urls
log_in        = 'accounts:login'
profile       = 'profiles:home'
adminstration = 'projects:adminstration'


## class to his name
from ProjectsLogs.models import (
    Added, 
    Removed, 
    Changed, 
    Deprecated, 
    Fixed, 
    Security
)

change_types = {
    'added': Added, 
    'removed': Removed, 
    'changed': Changed, 
    'deprecated': Deprecated, 
    'fixed': Fixed, 
    'security': Security
}