from archive_rotator import rotator
from archive_rotator.algorithms import TieredRotator


class GlacierBackupRotator:

    def __init__(self):
        pass

    def rotate(self, path, extension):
        rotator.rotate(
            TieredRotator([7, 4, 12], verbose=True),
            path,
            extension,
            verbose=True
        )
