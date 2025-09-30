"""
This file demonstrates a custom command that can be executed using "frepplectl".
"""

from optparse import make_option

# Always inherit from this base class.
from django.core.management.base import BaseCommand


class Command(BaseCommand):
  # Help text shown when you run "frepplectl help my_command"
  help = '''
  This is a sample command.
  '''

  # Options of the command
  option_list = BaseCommand.option_list + (
    make_option('--my_option', dest='my_option', type='string',
      help='My own option'),
    )

  requires_model_validation = False

  # Version number
  def get_version(self):
    return "0.1"

  # The code for the command
  def handle(self, *args, **options):
    print ("This command doesn't do anything... Really...")