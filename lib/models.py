# -*- coding: utf-8 -*-
# models.py

from flask_login import UserMixin
import json
from lib.manager import login_manager
PROFILE_FILE = "admin/profiles.json"

class User(UserMixin):
    pass

def query_user(username):
    usr_dic = []
    with open(PROFILE_FILE) as f:
        user_profiles = json.load(f)
        usr_dic = user_profiles
    if usr_dic:
        for usr in usr_dic:
            if usr["name"] == username:
                return usr

@login_manager.user_loader
def load_user(username):
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id = username
        return curr_user