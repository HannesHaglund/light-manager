from .utilities.connection import toggle_light
from .utilities.config import Config

def do(config_file, dry_run):
    conf = Config(config_file)
    for lid in conf.lights():
        info = conf.light_info(lid)
        if not dry_run:
            toggle_light(info.hostname, \
                         info.port, \
                         info.light_id, \
                         conf.light_on(lid))
