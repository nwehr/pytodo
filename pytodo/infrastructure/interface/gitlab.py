from __future__ import annotations

import requests
import json
import sys

from pytodo.termcolor import termcolor
from pytodo.core.domain.issue import Issue
from pytodo.core.domain.issue import Interface

class Gitlab(Interface):
    base_url: str
    headers: dict[str, str]

    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.headers = {"PRIVATE-TOKEN": auth_token}

    def add_issue(self, title: str):
        uri = "/issues"
        response = requests.post(self.base_url + uri, json={"title": title}, headers=self.headers)
        
        if response.status_code - 200 > 99:
            print(termcolor.FAIL + response.text)
            sys.exit(1)

    def remove_issue(self, id: int):
        uri = "/issues/{}".format(id) 
        response = requests.delete(self.base_url + uri, headers=self.headers)

        if response.status_code - 200 > 99:
            print(termcolor.FAIL + response.text)
            sys.exit(1)

    def close_issue(self, id: int):
        uri = "/issues/{}".format(id) 
        response = requests.put(self.base_url + uri, json={"state_event": "close"}, headers=self.headers)

        if response.status_code - 200 > 99:
            print(termcolor.FAIL + response.text)
            sys.exit(1)
            
    def open_issue(self, id: int):
        uri = "/issues/{}".format(id) 
        response = requests.put(self.base_url + uri, json={"state_event": "reopen"}, headers=self.headers)

        if response.status_code - 200 > 99:
            print(termcolor.FAIL + response.text)
            sys.exit(1)

    def get_issues(self, state: str = "open") -> list[Issue]:
        if state == "open":
            state = "opened"

        uri = "/issues?state={}".format(state)
        response = requests.get(self.base_url + uri, headers=self.headers)

        if response.status_code - 200 > 99:
            print(termcolor.FAIL + response.text)
            sys.exit(1)

        issues: list[Issue] = []

        for raw_issue in json.loads(response.text):
            issues.append(Issue(raw_issue["iid"], raw_issue["title"], raw_issue["state"]))

        return issues
