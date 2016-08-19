from shutil import copyfile
from os.path import normpath, isdir, basename
from os import remove
import lzma
import tarfile


class GlacierBackup:

    def __init__(self, parser, rotator, cloud_driver):
        self.args = parser.get_args()
        self.rotator = rotator
        self.cloud_driver = cloud_driver

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

        # self.cloud_driver.upload(self.args.vault, file)
        self.rotator.rotate(file_copy, extension)

        # Clean up
        for working_file in to_delete:
            remove(working_file)

    def compress(self, file):
        with lzma.open(file + '.xz', 'w') as outfile:
            with open(file, 'rb') as infile:
                outfile.write(infile.read())
        return file + '.xz'
