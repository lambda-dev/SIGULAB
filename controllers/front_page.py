# -*- coding: utf-8 -*-
# try something like
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def index():
    return dict()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def sustancias():
    return dict()
    
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def desechos():
    return dict()
