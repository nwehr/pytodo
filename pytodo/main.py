#
# Copyright (c) Nathan Wehr <nathan@wehrholdings.com>, All rights reserved.
#

from __future__ import annotations

import os
import sys
import yaml
import json
import requests

from pytodo.termcolor import termcolor
from pytodo.core.domain.issue import Issue
from pytodo.core.domain.issue import Interface
from pytodo.core.domain.comment import Comment

from pytodo.infrastructure.interface.github import Github
from pytodo.infrastructure.interface.gitlab import Gitlab

def main():
    config_path = os.getcwd() + "/.pytodo.yml"
    interface: Interface

    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        schema = input("schema [github]: ")
        
        print()
        print("  example base urls")
        print()
        print("  https://api.github.com/repos/{owner}/{repo}")
        print("  https://gitlab.com/api/v4/projects/{project_id}")
        print()

        base_url = input("base url: ")
        auth_token = input("auth token: ")

        config = {
            "schema": schema
            , "baseUrl": base_url
            , "authToken": auth_token
        }

        
        with open(config_path, "w+") as f:
            f.truncate()
            yaml.dump(config, f)

        sys.exit(0)

    if os.path.exists(config_path) == False:
        print("run `pyt -i` to initialize")
        sys.exit(0)

    with open(config_path) as f:
        for contents in yaml.load_all(f, Loader=yaml.FullLoader):
            schema = contents.get("schema", "github")
            
            if schema == "gitlab":
                interface = Gitlab(contents["baseUrl"], contents["authToken"])
            else:
                interface = Github(contents["baseUrl"], contents["authToken"])

    if len(sys.argv) > 1:
        if sys.argv[1] == "-a":
            interface.add_issue(sys.argv[2])
            sys.exit(0)

        if sys.argv[1] == "-r":
            interface.remove_issue(sys.argv[2])
            sys.exit(0)

        if sys.argv[1] == "-c":
            interface.close_issue(sys.argv[2])
            sys.exit(0)

        if sys.argv[1] == "-o":
            interface.open_issue(sys.argv[2])
            sys.exit(0)

    open_issues = interface.get_issues()
    closed_issues = interface.get_issues("closed")

    open_issues.sort(key = lambda x: x.id)
    closed_issues.sort(key = lambda x: x.id)

    for issue in open_issues:
        print("   {}. {}".format(issue.id, issue.title))

        if len(issue.comments) > 0:
            print()

        for comment in issue.comments:
            print('\x1B[3m', end="")
            print("      {}".format(comment.body))
            print("      - {}".format(comment.author))
            print('\x1B[23m')

    for issue in closed_issues:
        print(termcolor.GREEN + " ✓ {}. {}".format(issue.id, issue.title))
    
if __name__ == "__main__":
    main()

