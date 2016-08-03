from argparse import ArgumentParser
import boto3
import os
import lzma


class GlacierBackup:

    def __init__(self):
        self.setup_parser()
        self.get_aws_credentials()
        self.setup_glacier_client()

    def setup_parser(self):
        self.parser = ArgumentParser(description='Maintain backups of archives locally and on Amazon Glacier')
        self.parser.add_argument('--vault', metavar='V', help='the name of the Glacier vault in which to store the archive')
        self.parser.add_argument('file', help='file to generate archive from')
        self.args = self.parser.parse_args()

    def setup_glacier_client(self):
        self.glacier_client = boto3.client('glacier')

    def get_aws_credentials(self):
        self.access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        self.secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        self.default_region = os.environ['AWS_DEFAULT_REGION']

    def usage(self):
        self.parser.print_help()

    def backup(self):
        bytes = self.get_target_bytes()
        self.create_archive(bytes)
        self.upload_to_glacier()

    def get_target_bytes(self):
        with open(self.args.file, 'r') as infile:
            return infile.read().encode('utf-8')

    def create_archive(self, bytes):
        with lzma.open(self.args.file + '.xz', 'w') as outfile:
            outfile.write(bytes)

    def upload_to_glacier(self):
        archive_id = self.glacier_client.upload_archive(
            vaultName=self.args.vault,
            archiveDescription='Test',
            body=self.args.file + '.xz'
        )
        print('Uploaded archive: ', archive_id)

backup = GlacierBackup()
backup.backup()
