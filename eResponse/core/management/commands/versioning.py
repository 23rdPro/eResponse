"""
This is an automated process consisted in the git workflow from add to push.
"""
import logging
import subprocess
import shlex
import os
from abc import ABC
from argparse import ArgumentParser
from typing import List
from django.core.management.base import BaseCommand, CommandError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eResponse.settings')


class Command(BaseCommand, ABC):
    help = "adds, commits, and pushes multiple changes"

    def add_arguments(self, parser: ArgumentParser):
        pass

    @property
    def read_status_to_list(self) -> List[str]:
        with open('git.txt', 'w+') as temp:
            status = subprocess.Popen(['git', 'status'], stdout=temp)
            status.wait()

            statuses = [line.split()[-1] for line in temp.readlines()
                        if 'modified:' in line
                        ]
        # remove file when done
        if os.path.isfile('git.txt'):
            os.remove('git.txt')

        return statuses

    def handle(self, *args, **options):
        try:
            files = self.read_status_to_list
            print(files)
            for file in files:
                add = subprocess.Popen(['git', 'add', file])
                add.wait()

                prompt = input("Enter commit message: ")
                commit = subprocess.Popen(['git', 'commit', '-m', prompt.strip()])
                commit.wait()

            push = subprocess.Popen(['git', 'push', '-u', 'origin', 'main'])
            push.wait()

            self.stdout.write(f"Successfully added {len(files)} files")

        except CommandError or Exception as error:
            logging.error(error)
