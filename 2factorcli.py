#!/usr/bin/env python3
"""
Allow generation of 2 factor auth tokens via cli

Usage:
    2factorcli.py [options] get <name>
    2factorcli.py [options] add <name> <secret> [<description>] [<padding>]
    2factorcli.py [options] list
    2factorcli.py [options] rename <name> <newname>
    2factorcli.py [options] set-description <name> <description>
    2factorcli.py [options] set-padding <name> <padding>

Options:
  -v, --vault=<path>            GPG vault of secrets        [default: ~/.2factorcli.gpg]
  --disable-agent               Disable using a GPG agent
  --fingerprint=<fingerprint>   Which fingerprint to use
"""


import docopt
import gnupg
import json
import onetimepass
import os
import sys


def update_vault(secrets, vault_path, fingerprint=None, use_agent=True):
    gpg = gnupg.GPG(use_agent=use_agent)
    if fingerprint is None:
        # See if there's only one loaded GPG key
        private_keys = gpg.list_keys(True)
        if len(private_keys) == 0:
            print("No private keys loaded?")
            sys.exit(1)
        if len(private_keys) != 1:
            print("More then one private key loaded.")
            print("--fingerprint is required")
            sys.exit(1)
        fingerprint = private_keys[0]['fingerprint']
        del private_keys

    with open(vault_path, 'w') as fp:
        data = json.dumps(secrets)
        data = gpg.encrypt(data, fingerprint)
        fp.write(str(data))


def load_vault(vault_path, use_agent=True):
    gpg = gnupg.GPG(use_agent=use_agent)
    secrets = {}
    if os.path.isfile(vault_path):
        with open(vault_path, 'r') as fp:
            data = fp.read()
            data = gpg.decrypt(data)
            secrets = json.loads(str(data))

    return secrets


def columnize(data):
    # Split input data by row and then on spaces
    rows = [line.strip().split(' ') for line in data.strip().split('\n')]

    # Reorganize data by columns
    cols = zip(*rows)

    # Compute column widths by taking maximum length of values per column
    col_widths = [max(len(value) for value in col) for col in cols]

    # Create a suitable format string
    fmt = ' '.join(['%%-%ds\t' % width for width in col_widths])

    # Format each row using the computed format
    data = ''
    for row in rows:
        data += fmt % tuple(row)
        data += "\n"
    return data


def main():
    args = docopt.docopt(__doc__, version='2factorcli 0.0.1')

    # Use agents?
    use_agent = True
    if args['--disable-agent']:
        use_agent = False

    # Unwritten defaults
    if args['<description>'] is None:
        args['<description>'] = ''
    if args['<padding>'] is None:
        args['<padding>'] = 6

    # Find the vault path
    vault_path = os.path.abspath(os.path.expanduser(args['--vault']))

    # Load secrets into memory
    secrets = load_vault(vault_path, use_agent)

    ###########################################################################
    # Commands!
    ###########################################################################

    if args['list']:
        data = "Name Description\n"
        data += "---- -----------\n"
        for name in sorted(secrets.keys()):
            data += "%s %s\n" % (name, secrets[name]['description'])
        print(columnize(data))
        sys.exit(0)

    ###########################################################################

    if args['add']:
        if args['<secret>'] is None:
            print("<secret> is required!")
            sys.exit(1)

        if args['<name>'] is None:
            print("<name> is required!")
            sys.exit(1)

        secrets[args['<name>']] = {
            'secret': args['<secret>'],
            'description': args['<description>'],
            'name': args['<name>'],
            'padding': args['<padding>'],
            }

        update_vault(secrets,
                     vault_path,
                     fingerprint=args['--fingerprint'],
                     use_agent=use_agent)
        sys.exit(0)

    ###########################################################################

    if args['rename']:
        secrets[args['<newname>']] = secrets[args['<name>']]
        del secrets[args['<name>']]
        update_vault(secrets,
                     vault_path,
                     fingerprint=args['--fingerprint'],
                     use_agent=use_agent)
        sys.exit(0)

    ###########################################################################

    if args['get']:
        if args['<name>'] not in secrets:
            print('%s is not a known site!' % args['<name>'])
            sys.exit(1)
        token = onetimepass.get_totp(secrets[args['<name>']]['secret'])
        token = str(token).zfill(secrets[args['<name>']]['padding'])
        print(token)
        sys.exit(0)

    ###########################################################################

    if args['set-description']:
        if args['<name>'] not in secrets:
            print('%s is not a known site!' % args['<name>'])
            sys.exit(1)
        secrets[args['<name>']]['description'] = args['<description>']
        update_vault(secrets,
                     vault_path,
                     fingerprint=args['--fingerprint'],
                     use_agent=use_agent)
        sys.exit(0)

    ###########################################################################

    if args['set-padding']:
        if args['<name>'] not in secrets:
            print('%s is not a known site!' % args['<name>'])
            sys.exit(1)
        secrets[args['<name>']]['padding'] = args['<padding>']
        update_vault(secrets,
                     vault_path,
                     fingerprint=args['--fingerprint'],
                     use_agent=use_agent)
        sys.exit(0)

    ###########################################################################

    print("Command is required!")
    sys.exit(1)


if __name__ == "__main__":
    gpg = None
    main()
