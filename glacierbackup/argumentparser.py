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
            'file',
            metavar='src',
            help='file to generate archive from'
        )
        self.parser.add_argument(
            'destination',
            metavar='dest',
            help='The path you wish to save backups to'
        )
		self.parser.add_argument(
            'description',
            metavar='desc',
            help='A description for the archive that will be stored in Amazon Glacer'
        )

    def get_args(self):
        return self.parser.parse_args()
