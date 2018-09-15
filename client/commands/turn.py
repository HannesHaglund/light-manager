from .utilities.config import Config
from .refresh import do as do_refresh

def do(config_file, light_id, new_state_str, dry_run):
    new_state = None
    if new_state_str == 'on':
        new_state = True
    elif new_state_str == 'off':
        new_state = False
    else:
        raise RuntimeError('State must be \'on\' or \'off\'')
    conf = Config(config_file)
    conf.turn_light(light_id, new_state)
    conf.write()
    do_refresh(config_file, dry_run)
