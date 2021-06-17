#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from git import Repo
from git.repo.fun import is_git_dir


class GitTool:

    def __init__(self, repo_url, path, env,remote_name='origin', username='', password='', gitport=22):
        """
        :param path: 需要是绝对路径
        :param env: 项目环境，默认是测试环境
        """
        self.base_path = path
        self.repo_url = repo_url
        self.proj_name = repo_url.split('/')[-1].rstrip('.git')
        self.proj_path = os.path.join(self.base_path, self.proj_name, env)
        self.remote_name = remote_name
        self.repo = None
        self.initial(username, password, gitport)

    def initial(self, username='', password='', gitport=22):
        """
        初始化git仓库
        :param repo_url:
        :param branch:
        :return:
        """
        if not os.path.exists(self.proj_path):
            os.makedirs(self.proj_path)

        if username and password and self.repo_url.startswith('http'):
            t = self.repo_url.split('://')
            self.repo_url = f'{t[0]}://{username}:{password}@{t[1]}'
        elif gitport != 22:
            t = self.repo_url.split(':')
            if t[0] != 'ssh':
                self.repo_url = f'ssh://{t[0]}:{gitport}/{t[1]}'

        git_local_path = os.path.join(self.proj_path, '.git')
        ssh_executable = os.path.join('/data/', 'mysshexe.sh')
        if not is_git_dir(git_local_path):
            self.repo = Repo.clone_from(self.repo_url, to_path=self.proj_path, branch='master', env={"GIT_SSH":'/data/mysshexe.sh'})
        else:
            self.repo = Repo(self.proj_path)
        with self.repo.git.custom_environment(GIT_SSH=ssh_executable):
            origin = self.repo.remotes.origin
            origin.pull('master')


    def branches(self):
        """
        获取所有分支
        :return:
        """
        branches = self.repo.remote().refs
        return [item.remote_head for item in branches if item.remote_head not in ['HEAD', ]]


    def commits(self):
        """
        获取所有提交记录
        :return:
        """
        commit_log = self.repo.git.log('--pretty={"commit":"%h","author":"%an","summary":"%s","date":"%cd"}',
                                       max_count=10,
                                       date='format:%Y-%m-%d %H:%M')
        log_list = commit_log.split("\n")
        return [eval(item) for item in log_list]

    def pull(self):
        self.repo = Repo(self.proj_path)
        return self.repo.remote().pull('master')

    def checkout(self, name):
        """本地创建指定分支并切换到该分支"""
        self.repo.git.checkout(name)

    def change_to_branch(self, branch):
        """
        切换分值
        :param branch:
        :return:
        """
        self.repo.git.checkout(branch)

    def change_to_commit(self, branch, commit):
        """
        切换commit
        :param branch:
        :param commit:
        :return:
        """
        self.change_to_branch(branch=branch)
        self.repo.git.reset('--hard', commit)

    def change_to_tag(self, tag):
        """
        切换tag
        :param tag:
        :return:
        """
        self.repo.git.checkout(tag)

    def get_commit_msg(self, branch, commit):
        """获取指定commit的注释"""
        for i in self.repo.iter_commits(branch):
            if i.hexsha == commit:
                return i.message.rstrip('\n')
