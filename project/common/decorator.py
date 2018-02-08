from functools import wraps

from django.shortcuts import render
from django.http import JsonResponse


error_msg = {
	'code': -1,
	'msg': "wrong method"
}

def post_method(func):
	@wraps(func)
	def _deco(request, *args, **kwargs):
		if request.method == 'POST':
			return func(request, *args, **kwargs)
		else:
			return JsonResponse( error_msg )
			
	return _deco		



def get_method(func):
	@wraps(func)
	def _deco(request, *args, **kwargs):
		if request.method == 'GET':
			return func(request, *args, **kwargs)
		else:
			return JsonResponse( error_msg )
	return _deco	




