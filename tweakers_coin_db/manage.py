import sys
from alembic import command
import argparse
from functools import wraps
import logging
import os
import sys
from alembic import __version__ as __alembic_version__
from alembic.config import Config as AlembicConfig
from alembic import command
from alembic.util import CommandError

class Manager(object):
	q_command = None

	def __init__(self, args, *kwargs):
		print(args)
		self.q_command = args

		super().__init__()

	def migrate(self):
		# command.revision(config, message, autogenerate=autogenerate, sql=sql,
		# 				 head=head, splice=splice, branch_label=branch_label,
		# 				 version_path=version_path, rev_id=rev_id)
		pass

	def run(self):

		for _cmd in self.q_command:
			cmd = getattr(self, _cmd, None)

			if cmd is None or not hasattr(cmd,'__call__'):
				print(_cmd, "관련 명령어가 없습니다.")
			else:
				cmd()

		pass

manager = Manager(sys.argv[1:])

if __name__ == '__main__':
	manager.run()
