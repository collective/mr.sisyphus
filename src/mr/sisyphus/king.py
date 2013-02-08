import argparse
import logging
import pkg_resources

logger = logging.getLogger("mr.sisyphus")

class King(object):

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
        

king = King()
