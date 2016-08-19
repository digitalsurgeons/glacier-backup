from argparse import ArgumentParser


class GlacierBackupArgumentParser:

    def __init__(self):
        self.parser = ArgumentParser(
            description='Maintain backups locally and on Amazon Glacier'
        )
        self.parser.add_argument(
            '--vault',
            metavar='V',
            help='The name of the Glacier vault in which to store the archive'
        )
        self.parser.add_argument(
            '--compress',
            help='Use compression on the archive/file',
            action="store_true"
        )
        self.parser.add_argument(
            '--destination',
            metavar='D',
            help='The path you wish to save backups to'
        )
        self.parser.add_argument(
            'file',
            help='file to generate archive from'
        )

    def get_args(self):
        return self.parser.parse_args()
