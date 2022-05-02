#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate a json log of a git repository.
"""

from __future__ import print_function

__author__ = 'Tavish Armstrong'
__email__ = 'tavisharmstrong@gmail.com'
__version__ = '0.2.3'

import json
import sys


# -------------------------------------------------------------------
# Main
def git2log(git_dir):
    logs = git2jsons(run_git_log(git_dir))
    return logs


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--git-dir',
        default=None,
        help='Path to the .git/ directory of the repository you are targeting'
    )
    parser.add_argument(
        '--output-dir',
        default=None,
        help='Path to the .git/ directory of the repository you are targeting'
    )
    args = parser.parse_args()
    # print(args.git_dir)

    git_dir = 'F:\\研究生生活\\青岛软件所\\开源软件供应链\项目进展\\arch smell\\dataset\\hadoop-hdfs\\.git'
    git_dir = args.git_dir
    output_dir = args.output_dir

    logs = git2jsons(run_git_log(git_dir))
    # print(logs)
    # return logs
    with open(output_dir, 'w', encoding='utf-8') as f:
        f.write(logs)


# -------------------------------------------------------------------
# Main API functions


def git2jsons(s):
    return json.dumps(list(parse_commits(s)), ensure_ascii=False)


def git2json(fil):
    return json.dumps(list(parse_commits(fil.read())), ensure_ascii=False)


# -------------------------------------------------------------------
# Functions for interfacing with git


def run_git_log(git_dir=None):
    '''run_git_log([git_dir]) -> File

    Run `git log --numstat --pretty=raw` on the specified
    git repository and return its stdout as a pseudo-File.'''
    import subprocess
    if git_dir:
        command = [
            'git',
            '--git-dir=' + git_dir,
            'log',
            '--numstat',
            '--pretty=raw'
        ]
    else:
        command = ['git', 'log', '--numstat', '--pretty=raw']
    raw_git_log = subprocess.Popen(
        command,
        stdout=subprocess.PIPE
    )
    if sys.version_info < (3, 0):
        return raw_git_log.stdout
    else:
        return raw_git_log.stdout.read().decode('utf-8', 'ignore')


import re

PAT_COMMIT = r'''
(
commit\ (?P<commit>[a-f0-9]+)\n
tree\ (?P<tree>[a-f0-9]+)\n
(?P<parents>(parent\ [a-f0-9]+\n)*)
(?P<author>author \s+(.+)\s+<(.*)>\s+(\d+)\s+([+\-]\d\d\d\d)\n)
(?P<committer>committer \s+(.+)\s+<(.*)>\s+(\d+)\s+([+\-]\d\d\d\d)\n)\n
(?P<message>
(\ \ \ \ .*\n)*
)
\n
(?P<numstats>
(^(\d+|-)\s+(\d+|-)\s+(.*)$\n)*
)
)
'''
RE_COMMIT = re.compile(PAT_COMMIT, re.MULTILINE | re.VERBOSE)


# -------------------------------------------------------------------
# Main parsing functions

def parse_commits(data):
    '''Accept a string and parse it into many commits.
    Parse and yield each commit-dictionary.
    This function is a generator.
    '''
    raw_commits = RE_COMMIT.finditer(data)
    for rc in raw_commits:
        full_commit = rc.groups()[0]
        parts = RE_COMMIT.match(full_commit).groupdict()
        parsed_commit = parse_commit(parts)
        yield parsed_commit


def parse_commit(parts):
    '''Accept a parsed single commit. Some of the named groups
    require further processing, so parse those groups.
    Return a dictionary representing the completely parsed
    commit.
    '''
    commit = {}
    commit['commit'] = parts['commit']
    commit['tree'] = parts['tree']
    parent_block = parts['parents']
    commit['parents'] = [
        parse_parent_line(parentline)
        for parentline in
        parent_block.splitlines()
    ]
    commit['author'] = parse_author_line(parts['author'])
    commit['committer'] = parse_committer_line(parts['committer'])
    commit['message'] = "\n".join(
        parse_message_line(msgline)
        for msgline in
        parts['message'].splitlines()
    )
    commit['changes'] = [
        parse_numstat_line(numstat)
        for numstat in
        parts['numstats'].splitlines()
    ]
    return commit


# -------------------------------------------------------------------
# Parsing helper functions

def parse_hash_line(line, name):
    RE_HASH_LINE = name + r' ([abcdef0-9]+)'
    result = re.match(RE_HASH_LINE, line)
    if result is None:
        return result
    else:
        return result.groups()[0]


def parse_commit_line(line):
    return parse_hash_line(line, 'commit')


def parse_parent_line(line):
    return parse_hash_line(line, 'parent')


def parse_tree_line(line):
    return parse_hash_line(line, 'tree')


def parse_person_line(line, name):
    RE_PERSON = name + r' (.+) <(.*)> (\d+) ([+\-]\d\d\d\d)'
    result = re.match(RE_PERSON, line)
    if result is None:
        return result
    else:
        groups = result.groups()
        name = groups[0]
        email = groups[1]
        timestamp = int(groups[2])
        timezone = groups[3]
        d_result = {
            'name': name,
            'email': email,
            'date': timestamp,
            'timezone': timezone,
        }
        return d_result


def parse_committer_line(line):
    return parse_person_line(line, 'committer')


def parse_author_line(line):
    return parse_person_line(line, 'author')


def parse_message_line(line):
    RE_MESSAGE = r'    (.*)'
    result = re.match(RE_MESSAGE, line)
    if result is None:
        return result
    else:
        return result.groups()[0]


def parse_numstat_line(line):
    RE_NUMSTAT = r'(\d+|-)\s+(\d+|-)\s+(.*)'
    result = re.match(RE_NUMSTAT, line)
    if result is None:
        return result
    else:
        (sadd, sdel, fname) = result.groups()
        try:
            return (int(sadd), int(sdel), fname)
        except ValueError:
            return (sadd, sdel, fname)


if __name__ == '__main__':
    main()
