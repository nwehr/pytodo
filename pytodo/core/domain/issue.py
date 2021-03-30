from __future__ import annotations
from pytodo.core.domain.comment import Comment

class Issue:
    id: int
    title: str
    state: str
    comments: list[Comment]

    def __init__(self, id: int, title: str, state: str, comments: list[Comment] = []):
        self.id = id
        self.title = title
        self.state = state
        self.comments = comments


class Interface:
    def add_issue(self, title: str):
        pass

    def remove_issue(self, id: int):
        pass

    def close_issue(self, id: int):
        pass

    def open_issue(self, id: int):
        pass

    def get_issues(self) -> list[Issue]:
        pass
