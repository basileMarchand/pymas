import argparse
import email.mime.application
import email.mime.multipart
import email.mime.text 
import email.utils
import getpass
import pathlib as pl 
import smtplib
import ssl
import sys 


from pymas.config import need_config, PyMasConfig, ConfigNotFound
from pymas.utils import zip_dir, logger, catch_send_exception

class PyMasApp:
    def __init__(self):
        logger.info("PYthon MAil Sender")
        self.installParser()
        self._config = PyMasConfig()

    def installParser(self):
        self._parser = argparse.ArgumentParser(prog='PYthon MAil Sender', usage="pymas")
        subparsers = self._parser.add_subparsers(dest='command')
        self._config = subparsers.add_parser('config', help='Configure your smtp account')
        for key in PyMasConfig.default.keys():
            self._config.add_argument(f"--{key}", help=f"Set {key} value in config")

        self._send = subparsers.add_parser("send", help="send email")
        self._send.add_argument("-r", "--recipient", type=str, required=True)
        self._send.add_argument("-s", "--subject", type=str, required=True)
        self._send.add_argument("-t", "--text", type=str, default="")
        self._send.add_argument("-a", "--attachements", nargs="*", type=str)
        
    def parse(self):
        args = self._parser.parse_args()

        cmd = f"cmd_{args.command}"
        if hasattr(self, cmd):
            try:
                getattr(self, cmd)(args)
            except Exception as e: 
                logger.error(e)

        else:
            print("Error")            

    def cmd_config(self, args: argparse.Namespace): 
        self._config.loadIfExists()
        for key, val in args.__dict__.items():
            if key in PyMasConfig.default.keys() and val is not None:
                self._config.set(key, val)

    @need_config
    @catch_send_exception 
    def cmd_send(self, args: argparse.Namespace):
        logger.info(f"Send message to {self._config.get('from_address')}")
        ## Build message 
        msg = email.mime.multipart.MIMEMultipart()
        msg['From'] = self._config.get("from_address")
        msg['To'] = args.recipient
        msg['Date'] = email.utils.formatdate(localtime=True)
        msg['Subject'] = args.subject
        msg.attach( email.mime.text.MIMEText(args.text))

        ## Attach documents if required 

        if args.attachements is not None:
            for item in args.attachements:
                path = pl.Path(item)
                if path.is_dir():
                    zipname = zip_dir(path)
                    path = path.parent / zipname

                with path.open("rb") as fid:
                    part = email.mime.application.MIMEApplication(fid.read(),Name=path.name)
                part['Content-Disposition'] = f'attachment; filename="{path.name}"'
                msg.attach(part)

        
        context = ssl.create_default_context()
        try:
            password = getpass.getpass(prompt="Password: ", stream=None)
        except KeyboardInterrupt as e:
            print('', flush=True)
            logger.info("exit without send email")
            sys.exit(1)
        with smtplib.SMTP(self._config.get("smtp_server"), self._config.get("smtp_port")) as server:
            server.starttls(context=context)
            server.login(self._config.get("smtp_login"), password)
            server.send_message(msg)
            
        

    def hasConfig(self):
        return self._config.isValid()
