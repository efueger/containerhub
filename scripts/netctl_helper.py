#!/usr/bin/env python3

"""
netctl_helper: Adds or deletes netctl config files.

This program is part of containerhub and pretty useless outside of that project.

Usage:
  netctl_helper add <uuid>
  netctl_helper del <uuid>
  netctl_helper -h | --help
  netctl_helper --version

Options:
  -h --help        Show this help.
  --version        Show version.

Examples:
  Copy new profile from stdin:
  cat config | sudo netctl_helper add f2bd17b2-1942-41d9-9339-061f522949f0

  Delete a profile:
  sudo netctl_helper del ae899ccf-af59-44c7-9a70-fe11a76a56cb

  Dashes in UUID string are optional:
  cat config | sudo netctl_helper add f2bd17b2194241d99339061f522949f0
"""

import os
import sys
import uuid
import errno

from docopt import docopt


__author__ = 'Ricardo (XenGi) Band'
__copyright__ = 'Copyright 2016, Ricardo (XenGi) Band'
__credits__ = ['Ricardo (XenGi) Band']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Ricardo (XenGi) Band'
__email__ = 'email@ricardo.band'
__status__ = 'Development'


if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)

    try:
        network_uuid = uuid.UUID(args['<uuid>'], version=4)
    except ValueError:
        print('Not a valid UUIDv4. Doing nothing.', file=sys.stderr)
        sys.exit(1)

    if args['add']:
        network_profile_path = os.path.join('/etc/netctl', f'hubnet_{str(network_uuid)}')
        buf = sys.stdin.read()
        try:
            with open(network_profile_path, 'w') as f:
                f.write(buf)
        except IOError as e:
            if (e[0] == errno.EPERM):
                print('You need root permissions to do this!', file=sys.stderr)
                sys.exit(1)
            else:
                print(f'Unexpected error: {e}')

    elif args['del']:
        network_profile_path = os.path.join('/etc/netctl', f'hubnet_{str(network_uuid)}')
        if os.path.isfile(network_profile_path):
            try:
                os.unlink(network_profile_path)
            except IOError as e:
                if (e[0] == errno.EPERM):
                    print('You need root permissions to do this!', file=sys.stderr)
                    sys.exit(1)
                else:
                    print(f'Unexpected error: {e}')
        else:
            # The profile to be deleted is not there so the state that is to be achieved is already achived.
            # Because of that we print an error but exit successfully.
            print('Network profile doesn\'t exist.', file=sys.stderr)
