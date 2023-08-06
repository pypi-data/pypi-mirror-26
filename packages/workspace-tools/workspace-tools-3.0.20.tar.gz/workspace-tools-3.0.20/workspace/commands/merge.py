from __future__ import absolute_import
import logging
import sys
import textwrap

import click
import git

from workspace.config import config
from workspace.commands import AbstractCommand
from workspace.scm import checkout_branch, current_branch, merge_branch, repo_path


log = logging.getLogger(__name__)


class Merge(AbstractCommand):
    """
    Merge changes from branch to current branch

    :param str branch: The branch to merge from.
    :param bool downstreams: Merge current branch to downstream branches defined in config merge.branches
                             that are on the right side of the current branch value and pushes them to all remotes.
                             Branches on the left side are ignored and not merged.
    :param str strategy: The merge strategy to pass to git merge
    :param bool dry_run: Print out what will happen without making changes.

    """
    @classmethod
    def arguments(cls):
        _, docs = cls.docs()
        return [
          cls.make_args('branch', nargs='?', help=docs['branch']),
          cls.make_args('-d', '--downstreams', action='store_true', help=docs['downstreams']),
          cls.make_args('-s', '--strategy', help=docs['strategy']),
          cls.make_args('-n', '--dry-run', action='store_true', help=docs['dry_run']),
        ]

    def run(self):
        current = current_branch()
        repo = git.Repo(path=repo_path())

        if self.branch and self.downstreams:
            log.error('Branch and --downstreams are mutually exclusive. Please use one or the other.')
            sys.exit(1)

        if repo.is_dirty(untracked_files=True):
            log.error('Your repo has untracked or modified files in working dir or in staging index. Please cleanup before doing merge')
            sys.exit(1)

        if not self.skip_update:
          self.commander.run('update', quiet=True)

        if self.branch:
            click.echo('Merging {} into {}'.format(self.branch, current))

            if self.dry_run:
                self.show_commit_diff(repo, current, self.branch)
            else:
                merge_branch(self.branch, strategy=self.strategy)

        elif self.downstreams:
            if not config.merge.branches:
                log.error('Config merge.branches must be configured with a list of branches to merge to')
                sys.exit(1)

            branches = config.merge.branches.split()
            if current not in branches:
                log.error('Current branch %s not found in config merge.branches (%s)', current, config.merge.branches)
                sys.exit(1)

            last = current
            downstream_branches = branches[branches.index(last)+1:]

            if not downstream_branches:
                click.echo('You are currently on the last branch, so no downstream branches to merge.')
                click.echo('Switch to the branch that you want to merge from first, and then re-run')
                sys.exit(0)

            for branch in downstream_branches:
                click.echo('Merging {} into {}'.format(last, branch))
                checkout_branch(branch)

                if not self.skip_update:
                    self.commander.run('update', quiet=True)

                if self.dry_run:
                    self.show_commit_diff(repo, branch, last)

                else:
                    merge_branch(last, strategy=self.strategy)

                    if repo.branches[branch].commit != repo.remotes.origin.refs[branch].commit:
                        self.commander.run('push', all_remotes=True)
                    else:
                        click.echo('Already up-to-date.')

                last = branch

        else:
            log.error('Please specify either a branch to merge from or --downstreams to merge to all downstream branches')
            sys.exit(1)

    def show_commit_diff(self, repo, branch, from_branch):
        """ Show commit diffs between from_branch to branch """
        commits = repo.git.log('{}..{}'.format(branch, from_branch), oneline=True)
        if commits:
            click.echo('The following commit(s) would be merged:')
            click.echo(textwrap.indent(commits, '  '))
        else:
            click.echo('Already up-to-date.')
