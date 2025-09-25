import os
import psutil
from dicom_router.settings import DISK_STORAGE_PATH, MAX_DISK_USAGE
from pacs_server.repositories.nodes import is_authorized
from pynetdicom.events import Event
from loguru import logger


class Handler:
    # Event handler for association requests
    def handle_assoc(event):
        assoc = event.assoc
        # Check if sender is authorized
        if not is_authorized(assoc.requestor.ae_title, assoc.requestor.address):
            logger.warning(f"Unauthorized sender with AE Title and ip: {assoc.requestor.ae_title}, {assoc.requestor.address}")
            return 0x02  # Reject association
        return 0x00  # Accept association

    def handle_store(self, event: Event):
        """Handle EVT_C_STORE events."""

        disk_home = psutil.disk_usage(DISK_STORAGE_PATH)
        percentage_disk = disk_home[3]

        logger.debug("Saving instance {instance_uid} started!", instance_uid=event.request.AffectedSOPInstanceUID)

        if percentage_disk < MAX_DISK_USAGE:
            ds = event.dataset

            study_id = ds.get('StudyID', 'unknown_study')
            save_folder = os.path.join(DISK_STORAGE_PATH, study_id)
            os.makedirs(save_folder, exist_ok=True)
            file_path = os.path.join(save_folder, f"{event.request.AffectedSOPInstanceUID}.dcm")
            ds.save_as(file_path)

            return 0x0000

        else:
            self.__logger.log.warning(
                f"Disk usage is {percentage_disk} that means almost full. Ignore DICOM files without saving!")
            return 0x0000

    def handle_echo(self, event):
        requestor = event.assoc.requestor
        addr, port = requestor.address, requestor.port

        self.__logger.log.info(
            "Received C-ECHO request from {addr}:{port}", addr=addr, port=port)

        return 0x0000
