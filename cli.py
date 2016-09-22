#!/usr/bin/env python

import logging
from glacierbackup import *


def main():
    logging.getLogger(__name__)
    logging.basicConfig(
        # filename='glacer-backup.log',
        format='%(name)s:%(levelname)s:%(asctime)s: %(message)s',
        level=logging.WARNING
    )

    backup = GlacierBackup(
        GlacierBackupArgumentParser(),
        GlacierBackupRotator(),
        GlacierBackupGlacierClient()
    )

    backup.backup()

if __name__ == '__main__':
    main()
