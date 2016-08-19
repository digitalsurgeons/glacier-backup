import boto3


class GlacierBackupGlacierClient:

    def __init__(self):
        self.glacier_client = boto3.client('glacier')

    def upload(self, vault, file):
        archive_meta = self.glacier_client.upload_archive(
            vaultName=vault,
            archiveDescription='Test',
            body=file
        )
        print('Uploaded archive: ', archive_meta)
