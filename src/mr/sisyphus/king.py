import os
import argparse
import getpass
import logging
import pkg_resources
from ConfigParser import SafeConfigParser

import github3

logger = logging.getLogger("mr.sisyphus")

def find_base():
    path = os.getcwd()
    while path:
        if os.path.exists(os.path.join(path, 'mr.sisyphus.cfg')):
            break
        old_path = path
        path = os.path.dirname(path)
        if old_path == path:
            path = None
            break
    if path is None:
        raise IOError("mr.sisyphus.cfg not found")
    return path

class King(object):

    def create_token(self):
        gh = github3.GitHub()
        auth = None
        while auth is None:
            username = raw_input("Github Username: ")
            password = getpass.getpass("Github password: ")
            try:
                auth = gh.authorize(username, password, scopes=["user"], note="Mr. Sisyphus")
            except:
                logger.exception("Couldn't create oauth token")
        return auth
    
    def get_or_update_token_from_config(self):
        config = self.get_configuration()
        if config.has_option("sisyphus", "token"):
            token = config.get("sisyphus", "token", None)
        else:
            token = self.create_token().token
            config.set("sisyphus", "token", token)
            config_file_path = os.path.join(find_base(), "mr.sisyphus.cfg")
            with open(config_file_path, 'wb') as configfile:
                config.write(configfile)
        return token
    
    def get_configuration(self):
        config = os.path.join(find_base(), "mr.sisyphus.cfg")
        parser = SafeConfigParser()
        parser.read(config)
        return parser
    
    def __call__(self, **kwargs):
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(ch)
        
        self.parser = argparse.ArgumentParser()
        version = pkg_resources.get_distribution("mr.sisyphus").version
        self.parser.add_argument('-v', '--version',
                    action='version',
                    version='mr.sisyphus %s' % version)
        self.parser.add_argument("-n", help="Dry run, just print the calls that would be made", action="store_true")
        args = self.parser.parse_args()
        
        config = self.get_configuration()
        print self.get_or_update_token_from_config()

king = King()
