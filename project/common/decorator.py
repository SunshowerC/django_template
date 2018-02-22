from functools import wraps

from django.shortcuts import render
from django.http import JsonResponse

import logging

logger = logging.getLogger('root')

error_msg = {
	'code': -1,
	'msg': "wrong method",
}

def post_method(func):
    @wraps(func)
    def _deco(request, *args, **kwargs):
        if request.method == 'POST':
            return func(request, *args, **kwargs)
        else:
            error_msg['path'] = request.path
            return JsonResponse( error_msg )
			
    return _deco		


def get_method(func):
    @wraps(func)
    def _deco(request, *args, **kwargs):
        if request.method == 'GET':
            return func(request, *args, **kwargs)
        else:
            error_msg['path'] = request.path
            return JsonResponse( error_msg )
    return _deco	




def require_login():
    @wraps(func)
    def _deco(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Do something for authenticated users.
            logger.info('user login')
        else:
            # Do something for anonymous users.
            logger.info('user do not login')
    return _deco    


