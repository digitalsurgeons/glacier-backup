#!/usr/bin/env python

from argparse import ArgumentParser
import boto3
import lzma
from archive_rotator import rotator
from archive_rotator.algorithms import TieredRotator


class GlacierBackup:

    def __init__(self):
        self.setup_parser()
        self.setup_glacier_client()

    def setup_parser(self):
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
        self.args = self.parser.parse_args()

    def setup_glacier_client(self):
        self.glacier_client = boto3.client('glacier')

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

    def rotate(self, path, extension):
        rotator.rotate(
            TieredRotator([7, 4, 12], verbose=True),
            path,
            extension,
            verbose=True
        )

backup = GlacierBackup()
backup.backup()
