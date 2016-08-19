#!/usr/bin/env python

from glacierbackup import *


def main():
    backup = GlacierBackup(
        GlacierBackupArgumentParser(),
        GlacierBackupRotator(),
        GlacierBackupGlacierClient()
    )
    backup.backup()

main()
