# -*- coding: UTF-8 -*-
import git


class GitUtil:

    repo = None

    def __init__(self, repo_path):
        self.repo_path = repo_path

    def instance(self):
        GitUtil.repo = git.Repo(self.repo_path)

