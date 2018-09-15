from .utilities.config import Config
from datetime import datetime
import calendar
import colorama

def do(config_file, current_date, current_time, n):
    current_time = int(current_time)
    date_obj = datetime.strptime(current_date, '%Y%m%d')
    current_weekday = date_obj.weekday()
    conf = Config(config_file)
    events = conf.events_sorted()
    events_before = []
    events_after = []
    for event in events:
        day = int(event[0])
        time = int(event[1])
        if (day < current_weekday or (day == current_weekday and time < current_time)):
            events_before.append(event)
        else:
            events_after.append(event)
    events_reordered = events_after + events_before
    events_left = n
    for event in events_reordered:
        if events_left == 0:
            break
        day = int(event[0])
        time = event[1]
        lid = event[2]
        state = 'on' if bool(event[3]) else 'off'
        word_color = colorama.Fore.MAGENTA
        light_color = colorama.Fore.BLACK + colorama.Back.YELLOW
        padding_length = abs(len(calendar.day_name[day]) - max(len(e) for e in calendar.day_name))
        print(word_color + calendar.day_name[day] + colorama.Style.RESET_ALL + \
              ' '*padding_length + ' at ' + \
              word_color + time + colorama.Style.RESET_ALL + \
              ': Turn light ' + \
              light_color + '#' + lid + colorama.Style.RESET_ALL + \
              ' ' + state + '.')
        events_left -= 1
