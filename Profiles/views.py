# Create your views here.
from django.http import HttpResponse
from .models import UserProfile
from functions import (
    # my functions
    get_object,
    this_is_admin, 
    is_logined,
    Home,
    # builtin django
    render,
    redirect,
    slugify,
)

from constants import (
    log_in,
    profile,
)

# Create your views here.

## helper function not main view function
def load_profile(request, slug, context={}):
    """ to load user profile throw the slug """
    profile = get_object(UserProfile,slug=slug)
    if profile:
        context.update({
            'profile' : profile,
            'user'    : profile.user, ## forignkey
            'projects': profile.user_projects.all(), ## ManyToMany
        })
        return render(request, 'profile.html', context)

    else:
        return HttpResponse('there is no profile for this user<br> contact with us')

def OpenProfile(request, slug):
    """ user can only open his profile """

    ## first check he is logined
    if is_logined(request):

        ## check if he ask for his profile 
        # else see if he admin else redirect to his profile
        user    = request.user.username
        if slug == slugify(user):
            ## load his profile
            return load_profile(request, slug)
        else:
            if this_is_admin(request):
                ## load profile as admin give u access to create projects
                context = {'admin': True}
                return load_profile(request, slug, context)
                
            else:
                ## someone try to access other redirect him to his profile
                return redirect(profile)
    else:
        ## not logined has no access to any profile
        return redirect(log_in)