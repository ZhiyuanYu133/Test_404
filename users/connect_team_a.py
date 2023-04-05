#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import traceback

import requests
from requests.auth import HTTPBasicAuth

TEAM_A_URL = "https://cmput404-project-data.herokuapp.com"
TEAM_A_AUTH = {
    "username": "username1",
    "password": "123"
}


def get_team_a_users():
    url = TEAM_A_URL + "/service/authors"
    items = []
    try:
        data = requests.get(url, auth=HTTPBasicAuth(TEAM_A_AUTH["username"], TEAM_A_AUTH["password"]))
        if data.status_code == 200:
            team_a_auths = json.loads(data.text)
            items = team_a_auths["items"]
            for item in items:
                item["team"] = "A"
                item["node"] = TEAM_A_URL
                print(item)
    except:
        print(traceback.format_exc())
    finally:
        return items


def get_team_a_posts():
    url = TEAM_A_URL + "/service/posts"
    ret = []
    try:
        data = requests.get(url, auth=HTTPBasicAuth(TEAM_A_AUTH["username"], TEAM_A_AUTH["password"]))
        if data.status_code == 200:
            team_a_posts = json.loads(data.text)
            items = team_a_posts["items"]
            for item in items:
                if not item["visibility"] == "PUBLIC":
                    continue
                item["image"] = ""
                item["team"] = "A"
                item["node"] = TEAM_A_URL
                print(item)
                ret.append(item)
    except:
        print(traceback.format_exc())
    finally:
        return ret


def put_team_a_followers(profile, foreign_pk):
    ret = []
    url = TEAM_A_URL + "/service/authors/{}/followers/{}/".format(profile, foreign_pk)
    try:
        data = requests.put(url, auth=HTTPBasicAuth(TEAM_A_AUTH["username"], TEAM_A_AUTH["password"]))
        # print(data.status_code)
        # print(data.text)
        data = requests.delete(url, auth=HTTPBasicAuth(TEAM_A_AUTH["username"], TEAM_A_AUTH["password"]))
        # print(data.status_code)
        # print(data.text)
    except:
        print(traceback.format_exc())
    finally:
        return ret


if __name__ == '__main__':
    # get_team_a_users()
    # get_team_a_posts()
    put_team_a_followers(
        "18f4722f-cfa4-40ae-a31f-30ef7e36a5ae",
        "ebccc4ec-bd63-45ce-81bb-0b38dfcf20de"
    )
    pass
