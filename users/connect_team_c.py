#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import traceback

import requests
from requests.auth import HTTPBasicAuth

TEAM_C_URL = "https://floating-fjord-51978.herokuapp.com"
TEAM_C_AUTH = {
    "username": "admin",
    "password": "admin"
}


def get_team_c_users():
    url = TEAM_C_URL + "/authors"
    items = []
    try:
        data = requests.get(url, auth=HTTPBasicAuth(TEAM_C_AUTH["username"], TEAM_C_AUTH["password"]))
        if data.status_code == 200:
            TEAM_C_auths = json.loads(data.text)
            items = TEAM_C_auths["items"]
            for item in items:
                item["team"] = "C"
                item["node"] = TEAM_C_URL
                print(item)
    except:
        print(traceback.format_exc())
    finally:
        return items


def get_auth_users():
    url = TEAM_C_URL + "/auth/users"
    items = []
    try:
        data = requests.get(url, auth=HTTPBasicAuth(TEAM_C_AUTH["username"], TEAM_C_AUTH["password"]))
        if data.status_code == 200:
            datas = json.loads(data.text)
            # items = datas["items"]
            for data in datas:
                print(data)
    except:
        print(traceback.format_exc())
    finally:
        return items

if __name__ == '__main__':
    # get_team_c_users()
    get_auth_users()
