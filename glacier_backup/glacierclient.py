import logging
import boto3


class GlacierBackupGlacierClient:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        try:
            self.glacier_client = boto3.client('glacier')
        except Exception as e:
            self.glacier_client = None
            self.logger.warning('No credentials found for upload to glacier')

    def upload(self, vault, file, description):
        if self.glacier_client is not None:
            archive_meta = self.glacier_client.upload_archive(
                vaultName=vault,
                archiveDescription=description,
                body=file
            )

            # Log successful upload to stdout
            self.logger.info(
                'Uploaded archive %s with glacier id %s to vault %s',
                file,
                archive_meta['archiveId'],
                vault
            )
