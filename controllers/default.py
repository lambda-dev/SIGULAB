# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def login():
     return dict(form=auth.login())
def register():
     return dict(form=auth.register())
def reset():
     return dict(form=auth.request_reset_password())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

