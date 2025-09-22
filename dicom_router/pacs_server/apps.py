from django.apps import AppConfig
from loguru import logger


class PacsServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pacs_server'

    def ready(self):
        from pacs_server.server import PACSServer
        from dicom_router import settings

        logger.info("Starting PACS Server...")
        pacs_server = PACSServer(settings.DICOM_PORT)
        pacs_server.start_server()
        logger.info(f"PACS Server started on port {settings.DICOM_PORT}")