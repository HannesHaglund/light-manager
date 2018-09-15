from .utilities.config import Config
from .refresh import do as do_refresh
from datetime import datetime

def do(config_file, date, time, dry_run):
    date_obj = datetime.strptime(date, '%Y%m%d')
    weekday = date_obj.weekday()
    conf = Config(config_file)
    conf.update_state(weekday, int(time))
    conf.write()
    do_refresh(config_file, dry_run)
