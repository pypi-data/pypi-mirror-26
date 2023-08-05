#!/usr/bin/env python3

import argparse
import subprocess
import sys


if sys.version_info < (3, 0): # NOQA pragma: no cover
    raise SystemError("Must be using Python 3")

__version__ = '0.2.0'
UBER = False


class FindReviewers():
    def get_reviewers(self):
        """
        All review classes should implement this and return a list of strings
        representing reviewers
        """
        raise NotImplementedError()

    def run_command(self, command):
        """ Wrapper for running external subprocesses """
        process = subprocess.run(command, stdout=subprocess.PIPE)
        data = process.stdout.decode("utf-8").strip()
        if data:
            return data.split('\n')
        return []

    def extract_username_from_email(self, email):
        """ Given an email, extract the username for that email """
        if UBER:
            if email[-9:] == '@uber.com':
                return email[:-9]
            else:
                return None
        return email


class FindFileLogReviewers(FindReviewers):
    def extract_username_from_shortlog(self, shortlog):
        """ Given a line from a git shortlog, extract the username """
        shortlog = shortlog.strip()
        email = shortlog[shortlog.rfind("<")+1:]
        email = email[:email.find(">")]
        username = self.extract_username_from_email(email)
        return username

    def get_log_reviewers_from_file(self, file_path):
        """ Find the reviewers based on the git log for a file """
        git_shortlog_command = ['git', 'shortlog', '-sne', file_path]
        git_shortlog = self.run_command(git_shortlog_command)
        users = [
            self.extract_username_from_shortlog(shortlog)
            for shortlog
            in git_shortlog
        ]
        users = [username for username in users if username]
        return users

    def get_changed_files(self):
        raise NotImplementedError()

    def get_reviewers(self):
        """ Find the reviewers based on the git log of the diffed files """
        changed_files = self.get_changed_files()
        reviewers = set()
        for changed in changed_files:
            users = self.get_log_reviewers_from_file(changed)
            reviewers = reviewers.union(users)
        return reviewers


class FindDiffLogReviewers(FindFileLogReviewers):
    def get_changed_files(self):
        """ Find the non-committed changed files """
        git_diff_files_command = ['git', 'diff-files', '--name-only']
        git_diff_files = self.run_command(git_diff_files_command)
        return git_diff_files


class FindLogReviewers(FindFileLogReviewers):
    def get_changed_files(self):
        """ Find the changed files between current status and master """
        git_diff_files_command = ['git', 'diff', 'master', '--name-only']
        git_diff_files = self.run_command(git_diff_files_command)
        return git_diff_files


def show_reviewers(reviewers):
    print(", ".join(reviewers))


def main():
    global UBER
    description = "Suggest reviewers for your diff.\n"
    description += "https://github.com/albertyw/git-reviewers"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--path',
        default='',
        help='relative path to the current git repository'
    )
    parser.add_argument(
        '--uber',
        action="store_true",
        help='output reviewers list to work with uber repositories'
    )
    args = parser.parse_args()
    UBER = args.uber

    finders = [FindDiffLogReviewers, FindLogReviewers]
    reviewers = set()
    for finder in finders:
        finder_reviewers = finder().get_reviewers()
        reviewers = reviewers.union(finder_reviewers)
    show_reviewers(reviewers)


if __name__ == "__main__":
    main()
