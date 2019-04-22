from django.contrib.auth import authenticate, login, logout
from functions import (
    # my functions
    is_logined,
    this_is_admin,
    err_msg,
    Home,

    # builtin django
    redirect, 
    render,
)

from constants import (
    adminstration,
    profile,
    log_in,
)

# Create your views here.


def Login(request):
    """ To login user and check if he is admin """

    ## first check if he already logined and he try to XSS
    if is_logined(request):
        return redirect(profile)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        ## if there is match for username and password 
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            ## if admin who logined redirect him to adminstration page
            if this_is_admin(request):
                return redirect(adminstration)

            return redirect(profile)
        else:
            err_msg(
                request, 
                'username or password is incorrect'
            )
            return redirect(log_in)

    else:
        return render(request, 'login.html')

def Logout(request):
    """ logout if logined else redirect to login page """
    if is_logined(request):
        logout(request)
    return redirect(log_in)



# ## class based view
# from django.utils.http import is_safe_url
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import never_cache
# from django.views.decorators.csrf import csrf_protect
# from django.views.decorators.debug import sensitive_post_parameters
# from django.views.generic import FormView, RedirectView

# class LoginView(FormView):
#     """
#     Provides the ability to login as a user with a username and password
#     """
#     success_url = '/auth/home/'
#     form_class = AuthenticationForm
#     redirect_field_name = REDIRECT_FIELD_NAME

#     @method_decorator(sensitive_post_parameters('password'))
#     @method_decorator(csrf_protect)
#     @method_decorator(never_cache)
#     def dispatch(self, request, *args, **kwargs):
#         # Sets a test cookie to make sure the user has cookies enabled
#         request.session.set_test_cookie()

#         return super(LoginView, self).dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         auth_login(self.request, form.get_user())

#         # If the test cookie worked, go ahead and
#         # delete it since its no longer needed
#         if self.request.session.test_cookie_worked():
#             self.request.session.delete_test_cookie()

#         return super(LoginView, self).form_valid(form)

#     def get_success_url(self):
#         redirect_to = self.request.POST.get(self.redirect_field_name)
#         if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
#             redirect_to = self.success_url
#         return redirect_to
