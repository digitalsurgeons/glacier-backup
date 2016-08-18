#!/usr/bin/env python

from argparse import ArgumentParser
from shutil import copyfile
from os.path import normpath, isdir, basename
from os import remove
import boto3
import lzma
import tarfile
from archive_rotator import rotator
from archive_rotator.algorithms import TieredRotator


class GlacierBackup:

    def __init__(self):
        self.setup_parser()
        self.setup_glacier_client()

    def setup_parser(self):
        parser = ArgumentParser(
            description='Maintain backups locally and on Amazon Glacier'
        )
        parser.add_argument(
            '--vault',
            metavar='V',
            help='The name of the Glacier vault in which to store the archive'
        )
        parser.add_argument(
            '--compress',
            help='Use compression on the archive/file',
            action="store_true"
        )
        parser.add_argument(
            '--destination',
            metavar='D',
            help='The path you wish to save backups to'
        )
        parser.add_argument(
            'file',
            help='file to generate archive from'
        )
        self.args = parser.parse_args()

    def setup_glacier_client(self):
        self.glacier_client = boto3.client('glacier')

    def backup(self):
        to_delete = []

        # Tar it up if its a directory
        if isdir(self.args.file):
            file = self.args.file + '.tar'
            extension = '.tar'
            with tarfile.open(file, "w") as tar:
                tar.add(self.args.file)
                tar.close()
            to_delete.append(file)
        else:
            file = self.args.file
            extension = ''

        # Compress it if asked to
        if self.args.compress:
            file = self.compress(file)
            extension += '.xz'
            to_delete.append(file)

        file_copy = copyfile(
            file,
            normpath(self.args.destination + '/' + basename(file))
        )

        self.rotate(file_copy, extension)
        # self.upload_to_glacier(self.args.vault, file)

        # Clean up
        for working_file in to_delete:
            remove(working_file)

    def compress(self, file):
        with lzma.open(file + '.xz', 'w') as outfile:
            with open(file, 'rb') as infile:
                outfile.write(infile.read())
        return file + '.xz'

    def upload_to_glacier(self, vault, file):
        archive_id = self.glacier_client.upload_archive(
            vaultName=vault,
            archiveDescription='Test',
            body=file
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
