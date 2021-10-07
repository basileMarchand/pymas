
import logging
import pathlib as pl 
import sys
import zipfile

logger = logging.getLogger()
logger.setLevel(logging.INFO)
termHandler = logging.StreamHandler()
termHandler.setLevel(logging.INFO)
logger.addHandler(termHandler)


def zip_append(path: pl.Path, zip: zipfile.ZipFile):
    for item in path.iterdir():
        if item.is_file():
            zip.write(str(item), str(item))
        else:
            zip_append(item, zip)

def zip_dir(directory: pl.Path):
    zipname = directory.name + ".zip"
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Use glob instead of iterdir(), to cover all subdirectories.
        zip_append(directory, zipf)
        """
        for item in directory.iterdir():
            if item.is_file():
                zipf.write(str(item), str(item))
        """
    return zipname

from smtplib import SMTPAuthenticationError, SMTPHeloError

def catch_send_exception( func ):
    def internal(klass, *args):
        try:
            func(klass, *args)
        except SMTPHeloError as e:
            logger.info("connection to smtp server fail")
        except SMTPAuthenticationError as e:
            logger.error("SMTP credentials invalid")
        else:
            logger.info("mail sent")
    return internal
