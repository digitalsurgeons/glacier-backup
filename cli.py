#!/usr/bin/env python

from glacierbackup import *


def main():
    backup = GlacierBackup(
        GlacierBackupArgumentParser(),
        GlacierBackupRotator(),
        GlacierBackupGlacierClient()
    )
    backup.backup()

if __name__ == '__main__':
    main()
