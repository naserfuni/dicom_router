import os
from typing import List
from core.handler import Handler
from lib.logger import Logger
from pynetdicom.sop_class import Verification

from pynetdicom import (AE, debug_logger, evt, AllStoragePresentationContexts)


class PACSServer:
    def __init__(self, logger: Logger, dicom_port: int) -> None:
        self.__logger = logger
        self.__dicom_port = dicom_port
        self.__SUPPORTED_TRANSFER_SYNTAX: List[str] = [
            '1.2.840.10008.1.2',  # Implicit VR Little Endian,
            '1.2.840.10008.1.2.1',  # Explicit VR Little Endian,
            '1.2.840.10008.1.2.1.99',  # Deflated Explicit VR Little Endian
            '1.2.840.10008.1.2.2',  # Explicit VR Big Endian
            '1.2.840.10008.1.2.4.50',  # JPEG Baseline (JPEG 8-bit)
            '1.2.840.10008.1.2.4.51',  # JPEG Baseline (JPEG 12-bit)
            '1.2.840.10008.1.2.4.57',  # JPEG Lossless, Nonhierarchical
            # JPEG Lossless (Used for CR, US and Secondary Capture Image Storage)
            '1.2.840.10008.1.2.4.70',
            '1.2.840.10008.1.2.4.80',  # JPEG-LS Lossless Image Compression
            # JPEG-LS Lossy (Near- Lossless) Image Compression
            '1.2.840.10008.1.2.4.81',
            # JPEG 2000 Image Compression (Lossless Only)
            '1.2.840.10008.1.2.4.90',
            '1.2.840.10008.1.2.4.91',  # JPEG 2000 Image Compression
            # JPEG 2000 Part 2 Multicomponent Image Compression (Lossless Only)
            '1.2.840.10008.1.2.4.92',
            '1.2.840.10008.1.2.4.93',  # JPEG 2000 Part 2 Multicomponent Image Compression
            '1.2.840.10008.1.2.4.94',  # JPIP Referenced
            '1.2.840.10008.1.2.4.95',  # JPIP Referenced Deflate
            '1.2.840.10008.1.2.5',  # RLE Lossless
            '1.2.840.10008.1.2.6.1',  # RFC 2557 MIME Encapsulation
            '1.2.840.10008.1.2.4.100',  # MPEG2 Main Profile Main Level
            '1.2.840.10008.1.2.4.102',  # MPEG-4 AVC/H.264 High Profile / Level 4.1
            '1.2.840.10008.1.2.4.103'  # MPEG-4 AVC/H.264 BD-compatible High Profile / Level 4.1
        ]

    def start_server(self):
        new_pid = os.fork()
        if new_pid == 0:
            try:
                debug_logger()

                handler = Handler(self.__logger)
                self.__logger.log.info(
                    " -----  DICOM RECEIVER FUNCTION  ----- ")
                handlers = [(evt.EVT_C_ECHO, handler.handle_echo),
                            (evt.EVT_C_STORE, handler.handle_mammography_store),
                            (evt.EVT_C_FIND, handler.handle_mammography_find)]

                ae = AE()
                ae.supported_contexts = AllStoragePresentationContexts
                ae.add_supported_context(Verification)

                for ctx in ae.supported_contexts:
                    ctx.transfer_syntax = self.__SUPPORTED_TRANSFER_SYNTAX[:]

                self.__logger.log.success(
                    "DICOM SERVER RUNNING ON PORT [  %s  ]" % self.__dicom_port)
                self.__logger.log.success("STARTING AE SERVER... ")
                scp = ae.start_server(
                    ('', self.__dicom_port), block=True, evt_handlers=handlers)

                ae.QuitOnKeyboardInterrupt()

            except (KeyboardInterrupt, SystemExit) as err:
                self.__logger.log.exception(
                    'DICOM EXITED OR KEYBOARD INTERRUPT', err)
