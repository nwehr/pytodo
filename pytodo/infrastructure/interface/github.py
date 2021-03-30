from __future__ import annotations

import json
import sys
import requests

from pytodo.termcolor import termcolor
from pytodo.core.domain.issue import Issue
from pytodo.core.domain.issue import Interface
from pytodo.core.domain.comment import Comment

class Github(Interface):
    base_url: str
    headers: dict[str, str]

    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.headers = {"Authorization": "token " + auth_token}

    def add_issue(self, title: str):
        uri = "/issues"
        response = requests.post(self.base_url + uri, json={"title": title}, headers=self.headers)

        if response.status_code - 200 > 99:
            print(termcolor.FAIL + response.text)
            sys.exit(1)

    def remove_issue(self, id: int):
        print("not supported")

    def close_issue(self, id: int):
        uri = "/issues/{}".format(id) 
        response = requests.patch(self.base_url + uri, json={"state": "closed"}, headers=self.headers)

        if response.status_code - 200 > 99:
            print(termcolor.FAIL + response.text)
            sys.exit(1)

    def open_issue(self, id: int):
        uri = "/issues/{}".format(id) 
        response = requests.patch(self.base_url + uri, json={"state": "open"}, headers=self.headers)

        if response.status_code - 200 > 99:
            print(termcolor.FAIL + response.text)
            sys.exit(1)


    def get_issues(self, state: str = "open") -> list[Issue]:
        uri = "/issues?state={}".format(state)
        response = requests.get(self.base_url + uri, headers=self.headers)

        if response.status_code - 200 > 99:
            print(termcolor.FAIL + response.text)
            sys.exit(1)

        issues: list[Issue] = []

        for raw_issue in json.loads(response.text):
            comments = []
            
            if raw_issue["comments"] > 0:
                comments_response = requests.get(self.base_url + "/issues/{}/comments".format(raw_issue["number"]), headers=self.headers)

                for raw_comment in json.loads(comments_response.text):
                    comments.append(Comment(raw_comment["user"]["login"], raw_comment["body"].replace("\n", "\n      ")))

            issues.append(Issue(raw_issue["number"], raw_issue["title"], raw_issue["state"], comments))

        return issues
