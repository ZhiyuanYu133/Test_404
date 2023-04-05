#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import traceback

import requests
from requests.auth import HTTPBasicAuth

TEAM_B_URL = "https://cmput404-group-project.herokuapp.com"
TEAM_B_AUTH = {
    "username": "remote",
    "password": "remote"
}


def get_team_b_users():
    url = TEAM_B_URL + "/authors"
    items = []
    try:
        data = requests.get(url, auth=HTTPBasicAuth(TEAM_B_AUTH["username"], TEAM_B_AUTH["password"]))
        if data.status_code == 200:
            print(data.text)
            data = json.loads(data.text)
            items = data["items"]
            for item in items:
                item["team"] = "B"
                item["node"] = TEAM_B_URL
                print(item)
    except:
        print(traceback.format_exc())
    finally:
        return items


if __name__ == '__main__':
    get_team_b_users()
