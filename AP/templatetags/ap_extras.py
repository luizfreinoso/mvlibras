'''
Created on 24/11/2015

@author: luiz
'''
from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    return value.decode('utf-8').split(arg)