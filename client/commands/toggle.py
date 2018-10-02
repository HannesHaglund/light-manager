from .utilities.config import Config
from .refresh import do as do_refresh

def do(config_file, light_id, dry_run):
    conf = Config(config_file)
    conf.turn_light(light_id, not conf.light_on(light_id))
    conf.write()
    do_refresh(config_file, dry_run)
