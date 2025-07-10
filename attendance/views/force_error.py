# attendance/views/force_error.py
from django.http import HttpResponseServerError

def force_error(request):
    raise Exception("This is a test exception for 500 error.")
