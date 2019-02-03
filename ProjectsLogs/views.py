from django.http import HttpResponse
from functions import (
    # my functions
    is_logined,
    this_is_admin,
    get_object,
    redirect_prev_page,
    random_password,
    err_msg,
    Home,

    # builtin django
    reverse,
    redirect, 
    render,
)

from constants import (
    log_in,
    profile,
    change_types,
)

## models
from django.contrib.auth.models import User
from .models import Project, Version, Change, Comment
from Profiles.models import UserProfile

## forms
from .forms import CommentForm
from .forms import ProjectForm

## helpers
from json import loads

def has_access_to_project(request, project_slug):
    """ return project and context whitch tell he is admin or not"""
    if this_is_admin(request):
        context = {'admin': True}
        project = get_object(Project, slug=project_slug) ## get object or return None

    else:
        ## dont search in all projects just user's
        user_projects =  get_object(UserProfile, user=request.user)
        user_projects = user_projects.user_projects.all()
        has_access    = [project for project in user_projects if project.slug == project_slug]
        
        project = has_access.pop() if has_access else None
        context = {}

    return project, context

# Create your views here.
def OpenProject(request, slug):
    ## check he is_logined(request)
    if is_logined(request):
        ## be sure that user ask for his project or admin who ask
        project, context = has_access_to_project(request, slug)

        if project:
            versions= project.project_versions.all()
            comment_form = CommentForm()
            context.update({
                'project': project,
                'versions': versions,
                'comment_field': comment_form,
            })
            return render(request, 'project2.html', context)

        else:
            err_msg(request, 'You Dont Have Access For This Project')
            return redirect(profile)
    else:
        return redirect(log_in)

def SubmitComment(request, change_type, change_id):
    if is_logined(request):
        if request.method == 'POST':
            content = request.POST['content']

            ## add the comment to the table
            comment = Comment(content=content)
            comment.save()

            ## add the comment to the change
            Type = change_types[change_type]
            change = get_object(Type, id = change_id)
            change.user_notes.add(comment)

            return redirect_prev_page(request)
        else:
            return HttpResponse('this is not a post')
    else:
        return redirect(log_in)

def SubmitCommentReplay(request, comment_id):
    if is_logined(request):
        if request.method == 'POST':
            content = request.POST['content']

            ## add the comment to the table
            comment = get_object(Comment, id=comment_id)
            if comment and not comment.replay:
                clone_comment = comment
                clone_comment.replay = content
                
                comment = clone_comment
                comment.save()

            return redirect_prev_page(request)
        else:
            return HttpResponse('this is not a post')
    else:
        return redirect(log_in)


def Adminstration(request):
    if this_is_admin(request):
        context = {}

        if request.method == 'POST':
            ## this is create user from
            if request.POST.get('username'):
                ## get the field
                username = request.POST.get('username')
                ## check if exist already
                user = get_object(User, username=username)
                if not user:
                    password = random_password()
                    user     = User()
                    user.username = username
                    user.set_password(password)
                    user.save()
                
                    context.update({'password': password})

            ## this is search from
            if request.POST.get('search'):
                query = request.POST.get('search')
                search_type = request.POST.get('search-type')
                if search_type == 'user':
                    search_response = UserProfile.objects.filter(user__username__startswith=query)
                elif search_type == 'project':
                    search_response = Project.objects.filter(project_name__startswith=query)

                context.update({
                    'search_type': search_type,
                    'search_response': search_response,
                })

        ## - => to reverse the order
        profiles = UserProfile.objects.order_by('-user')
        projects = Project.objects.order_by('-created')
        context.update({
            'profiles': profiles,
            'projects': projects,
        })

        return render(request, 'adminstration.html', context)
    else:
        return redirect(profile)

def AddProject(request, profile_slug):
    if this_is_admin(request):
        if request.method == 'POST':
            ## save data
            ## get profile from user then save it
            profile = get_object(UserProfile, slug=profile_slug)
            if profile:
                ## create project
                add_project_form = ProjectForm(request.POST)
                if add_project_form.is_valid():
                    project = add_project_form.save()

                    ## add project to profile
                    profile.user_projects.add(project)
                
                    ## redirect to profile
                    user_link = reverse('profiles:profile', kwargs={'slug': profile_slug})
                    return redirect(user_link)

                else:
                    return redirect_prev_page(request)
            else:
                return HttpResponse('profile not found')

        elif request.method == 'GET':
            add_project_form = ProjectForm
            context = {
                'add_project_form': add_project_form,
            }
            return render(request, 'add-project.html', context)

## static function cuz its spesific case
def connect_change_and_version(version, change):
    """ this function to connet version  with its changes in its ManyToMany Fields """
    kind = change.kind
    
    if kind == 'added':
        version.added.add(change)
    elif kind == 'removed':
        version.removed.add(change)
    elif kind == 'changed':
        version.changed.add(change)
    elif kind == 'deprecated':
        version.deprecated.add(change)
    elif kind == 'fixed':
        version.fixed.add(change)
    elif kind == 'security':
        version.security.add(change)

def disconnect_change_and_version(version, change):
    """ this function to connet version  with its changes in its ManyToMany Fields """
    kind = change.kind
    
    if kind == 'added':
        version.added.remove(change)
    elif kind == 'removed':
        version.removed.remove(change)
    elif kind == 'changed':
        version.changed.remove(change)
    elif kind == 'deprecated':
        version.deprecated.remove(change)
    elif kind == 'fixed':
        version.fixed.remove(change)
    elif kind == 'security':
        version.security.remove(change)

def create_elm_in_table(Class, **kwargs):
    elm = Class(**kwargs)
    elm.save()

    return elm

def EditProject(request, project_slug):
    if this_is_admin(request):
        if request.method == 'POST':
            data = loads(request.POST['data'])
            
            ## change Original data of project
            project_org_data     = data['project_data']
            project              = get_object(Project, slug=project_slug)
            if project:
                project.project_name = project_org_data['project_name']
                project.breif        = project_org_data['brief']
                project.under_work   = project_org_data['worked_on']
                project.can_try      = project_org_data['can_try']
                project.finished     = project_org_data['finished']

                project.save()
                
                ## if i create new version
                if data['new_version']:
                    version_data = data['new_version']
                    version = create_elm_in_table(
                        Version,
                        version_number = version_data['version_number'],
                        critical_version = version_data['cretical'],
                        combitable_with_old_dependencies = version_data['combitable'],
                    )
                    project.project_versions.add(version)

                    version_changes = version_data['changes']
                    for change_type, values in version_changes.items():
                        Class = change_types[change_type]
                        for val in values:
                            change = create_elm_in_table(Class, explain= val)
                            connect_change_and_version(version, change)
                    
                ## if i edited an old version
                if data['old_version']:
                    version_data      = data['old_version']
                    editted_meta_data = version_data['editted_meta_data']
                    editted_changes   = version_data['editted_changes']
                    added_changes     = version_data['added_changes']

                    ## editted_meta_data : is dict of version id to its changes
                    for version_id, values in editted_meta_data.items():
                        version = get_object(Version, id=version_id)
                        if version:
                            version.version_number = values['version_number']
                            version.critical_version = values['cretical']
                            version.combitable_with_old_dependencies = values['combitable']

                            version.save()

                    ## editted_changes: change_id to change explain value
                    for version_id, values in editted_changes.items():
                        for val in values:
                            change_id = val['id']
                            value = val['val']
                        change = get_object(Change, id=change_id)
                        if change:
                            if value:
                                change.explain = value
                                change.save()
                            else:
                                version = get_object(Version, id=version_id)
                                disconnect_change_and_version(version, change)
                                
                    ## new_changes for old versions
                    for version_id, values in added_changes.items():
                        version = get_object(Version, id=version_id)
                        for val in values:
                            change_type = val['type']
                            Class = change_types[change_type]
                            change= create_elm_in_table(Class, explain = val['val'])

                            connect_change_and_version(version, change)
                

                url = reverse('projects:project', kwargs={'slug': project.slug})
                return redirect(url)

        else:
            project = get_object(Project, slug=project_slug)
            if project:
                context = {
                    'project': project,
                }
                return render(request, 'edit-project.html', context)
            else:
                return HttpResponse('there is no such project')
