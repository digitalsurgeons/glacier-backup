import boto3


class GlacierBackupGlacierClient:

    def __init__(self):
        try:
            self.glacier_client = boto3.client('glacier')
        except Exception as e:
            self.glacier_client = None
            print('warn: no credentials for upload to glacier')

    def upload(self, vault, file):
        if self.glacier_client is not None:
            archive_meta = self.glacier_client.upload_archive(
                vaultName=vault,
                archiveDescription='Test',
                body=file
            )

            # Log successful upload to stdout
            print(
                'Uploaded archive ',
                file,
                ' with glacier id ',
                archive_meta.archive_id,
                ' to vault ',
                vault
            )
