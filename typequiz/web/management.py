from django.core.signals import got_request_exception
import logging

def log(*args, **kwargs):
    logging.exception('error')

got_request_exception.connect(log)
