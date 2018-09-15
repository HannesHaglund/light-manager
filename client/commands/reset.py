import config.Config as Config
import refresh
import datetime

def do(config_file, date, time):
    date_obj = datetime.strptime(date, '%Y%m%d')
    weekday = date_obj.weekday()
    conf = Config(config_file)
    conf.update_state(weekday, int(time))
    conf.write()
    refresh.do(config_file)
