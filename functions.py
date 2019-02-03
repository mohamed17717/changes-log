from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse
from django.utils.text import slugify

from random import choice
from string import ascii_letters, digits

from constants import (
    log_in,
    adminstration
)

## repeated imports
from django.contrib import messages

## permissions ##
def this_is_admin(request):
    return request.user.is_superuser

def is_logined(request):
    return request.user.is_authenticated

## models data ##
def get_object(Class, **kwargs):
    try:
        return Class.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None

def redirect_prev_page(request):
    previous_path = '/'+ '/'.join(request.META.get('HTTP_REFERER').split('/')[3:])
    return redirect(previous_path)

def redirect_user_to_his_profile(request):
    """ there is condition that slug to profile is slugify from username """
    slug      = slugify(request.user.username)
    user_link = reverse('profiles:profile', kwargs={'slug': slug})
    return redirect(user_link)

## some fucntion
def pg(lst, pg_num, count = 20):
    """
        if you have much data and wanna to split them into pages
        you just pass data and a page number
    """
    index_until = pg_num*count 
    index_from  = index_until - count
    return lst[index_from: index_until]

def random_password(
            field  = ascii_letters + digits, 
            length = choice( range(10,13) ),
        ):
    """ generate str of rand length (10 => 12) """
    return ''.join( [choice(field) for i in range( length )] )

## views
def Home(request):
    """ check if logined (go profile) else redirect to login page """
    
    if is_logined(request):
        if this_is_admin(request):
            return redirect(adminstration)
        return redirect_user_to_his_profile(request)
    else:
        return redirect(log_in)

## msgs cus error msg need specific class
def err_msg(request, msg):
    ## danger is name in bootstrap
    messages.error(request, msg, 'danger')