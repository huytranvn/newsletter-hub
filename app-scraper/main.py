# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import click

from sources.python_weekly import PythonWeekly
from utils.logging import get_logger

logger = get_logger('main.py')

# The hashtable of sources.
source_map = {
    'python_weekly': PythonWeekly,
}


# Registry the group command.
@click.group()
@click.pass_context
def pip_cli(ctx, **kwargs):
    ctx.obj = kwargs


@pip_cli.command(name='run')
@click.option(
    '-s', '--source',
    required=True,
    type=str,
    help='The source of newsletter.',
)
@click.option(
    '-i', '--issue',
    required=False,
    type=int,
    help='The issue number.',
)
@click.option(
    '-t', '--to-issue',
    required=False,
    type=int,
    help='Get from issue 1 up until the given issue.',
)
def run(source: str, issue: int, to_issue):
    """
    Get source with a given issue.
    """


    if source in source_map:
        class_source = source_map[source]

        if not to_issue:
            # Getting 1 issue only.
            class_source(issue_number=issue).run()
        else:
            # Getting the whole issues from 1 to n.
            for i in range(1, to_issue):
                class_source(issue_number=i).run()

    logger.info(f'Getting source: {source} with issue: {issue}')


def main():
    pip_cli()


if __name__ == '__main__':
    pip_cli()
