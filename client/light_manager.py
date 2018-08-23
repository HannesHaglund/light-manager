import argparse
import sys
import csv
import math
import calendar
from datetime import datetime
import colorama

def valid_time_format(timestr):
    if len(timestr) != 4:
        return False
    h = int(timestr[1:2])
    m = int(timestr[3:4])
    if h < 0 or h > 24:
        return False
    if m < 0 or m > 59:
        return False
    return True

class Config:
    def __init__(self, path=None):
        self.path = path
        self.server_data = []
        self.events = []
        self.art = ""
        self.longitude = 0
        self.latitude = 0
        self.state = {}
        if path is not None:
            with open(path, 'r', newline="") as f:
                reader = csv.reader(f, delimiter=' ', quotechar='|')
                state = 0
                for row in reader:
                    if row == ['#location']:
                        state = 0
                    if row == ['#serverconf']:
                        state = 1
                    if row == ['#eventconf']:
                        state = 2
                    if row == ['#art']:
                        state = 3
                    if row == ['#temporarystate']:
                        state = 4
                    if not row[0].startswith('#'):
                        if state == 0:
                            self.latitude, self.longitude = (float(e) for e in row)
                        if state == 1:
                            self.server_data.append(row)
                        if state == 2:
                            self.events.append(row)
                        if state == 3:
                            if self.art == '':
                                self.art = row[0]
                            else:
                                self.art =  "\n" + self.art + row[0]
                        if state == 4:
                            self.state[int(row[0])] = (row[1] == 'True')
        for e in self.server_data:
            light = int(e[0])
            if light not in self.state:
                self.state[light] = False


    def update_state(self, up_to_day, up_to_time):
        events = self.events_sorted()
        for lid in self.lights():
            self.state[lid] = False
        for event in events:
            day = int(event[0])
            time = int(event[1])
            if day > up_to_day or (day == up_to_day and time > up_to_time):
                break
            lid = int(event[2])
            state = bool(event[3])
            self.state[lid] = state


    def events_sorted(self):
        events = sorted(self.events, key=lambda e: e[1])
        events = sorted(events, key=lambda e: e[0])
        return events


    def turn_light(self, light_id, state):
        self.state[light_id] = state


    def light_on(self, light_id):
        return self.state[light_id]


    def lights(self):
        return [k for (k, v) in self.state.items()]


    def write(self):
        with open(self.path, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['#location'])
            writer.writerow([self.latitude, self.longitude])
            writer.writerow(['#serverconf'])
            for e in self.server_data:
                writer.writerow(list(e))
            writer.writerow(['#eventconf'])
            for e in self.events:
                writer.writerow(list(e))
            writer.writerow(['#art'])
            writer.writerow([self.art])
            writer.writerow(['#temporarystate'])
            for k,v in self.state.items():
                writer.writerow([k, v])


def do_genconfig(output_path):
    def input_location_conf():
        print('-- LOCATION CONFIGURATION --')
        print('Enter:')
        print('>latitude, longitude')
        print('As floats.')
        inp = input('>').replace(' ', '').split(',')
        return [float(e) for e in inp]

    def input_server_conf():
        print('-- SERVER CONFIGURATION --')
        while True:
            print('Enter any number of ip adresses for light servers, separated by commas')
            servers = input('>').replace(" ", "").split(',')
            if servers:
                break
            else:
                print("Please enter at least one server.")
        rslt = []
        print("The following light ID's have been added:")
        for i, server in enumerate(servers):
            for j in range(3):
                light_id = i*3 + j
                print('#' + str(light_id) + ': Light number ' \
                      + str(j + 1) + ' on ' + server + '.')
                rslt.append( (light_id, server, j) )
        print("")
        return rslt

    def input_event_conf(valid_light_ids):
        rslt = []
        print('-- EVENT CONFIGURATION --')
        print('Enter the following any number of times. Enter empty line when you\'re done')
        print('> weekday, time, light-id, new-state')
        print('    weekday: int from 0-6, representing the days of the week, starting with Monday.')
        print('    time: Some time of the day, formatted as HHMM.')
        print('    light-id: The ID of the light to toggle at this time.')
        print('    new-state: New state of the light: \'on\' or \'off\'.')
        while True:
            print('Enter another event...')
            inp = input('>').replace(" ", "").split(',')
            if inp == ['']:
                break
            if len(inp) != 4:
                print('Error: The number of values must be 4.')
                continue
            weekday = int(inp[0])
            if weekday < 0 or weekday > 6:
                print('Error: Weekday out of range.')
                continue
            time = inp[1]
            if not valid_time_format(time):
                print('Error: Improper time format.')
                continue
            light_id = int(inp[2])
            if light_id not in valid_light_ids:
                valid_ids_str = '[%s]' % ', '.join(map(str, valid_light_ids))
                print('Error: Light id ' + str(light_id) + ' not valid.')
                print('Valid id\'s are: ' + valid_ids_str)
                continue
            state_str = inp[3]
            state = ( state_str == 'on' )
            if state_str != 'on' and state_str != 'off':
                print('Error: State needs to be \'on\' or \'off\'.')
                continue
            rslt.append( (weekday, time, light_id, state) )
        print("")
        return rslt

    location_conf = input_location_conf()
    server_conf = input_server_conf()
    valid_light_ids = list(set(e[0] for e in server_conf))
    event_conf = input_event_conf(valid_light_ids)

    conf = Config()
    conf.latitude = location_conf[0]
    conf.longitude = location_conf[1]
    conf.server_data = server_conf
    conf.events = event_conf
    conf.path = output_path
    conf.write()


def do_art(config_file):
    conf = Config(config_file)
    art_colorized = conf.art
    colorama.init()
    for light in conf.lights():
        if light < 0 or light > 9:
            # Multi-digit lights not yet supported
            continue
        light_str = str(light)
        color = (colorama.Back.YELLOW + colorama.Fore.BLACK) if conf.light_on(light) else colorama.Back.BLUE
        light_str_colored = color + \
                            light_str + \
                            colorama.Style.RESET_ALL
        art_colorized = art_colorized.replace(light_str, light_str_colored)
    white_character = 'w'
    white_colored = colorama.Back.WHITE + ' ' + colorama.Style.RESET_ALL
    art_colorized = art_colorized.replace(white_character, white_colored)
    cyan_character = 'c'
    cyan_colored = colorama.Back.CYAN + ' ' + colorama.Style.RESET_ALL
    art_colorized = art_colorized.replace(cyan_character, cyan_colored)
    print(art_colorized)


def do_set_art(config_file, art_file):
    with open(art_file) as f:
        art = f.read()
    conf = Config(config_file)
    conf.art = art
    conf.write()


def do_reset(config_file, date, time):
    date_obj = datetime.strptime(date, '%Y%m%d')
    weekday = date_obj.weekday()
    conf = Config(config_file)
    conf.update_state(weekday, int(time))
    conf.write()


def do_turn(config_file, light_id, new_state_str):
    new_state = None
    if new_state_str == 'on':
        new_state = True
    elif new_state_str == 'off':
        new_state = False
    else:
        print('Error: state must be \'on\' or \'off\'')
    conf = Config(config_file)
    conf.turn_light(light_id, new_state)
    conf.write()


def do_upcoming_events(config_file, current_date, current_time, n):
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


def main():
    parser = argparse.ArgumentParser(description='Manage indoor lighting.')
    subparsers = parser.add_subparsers(dest='command')

    genconfig = subparsers.add_parser('genconfig',
                                      description='Interactively generate a new config file.')
    genconfig.add_argument('output_path', metavar='output-path', type=str, help='System path to write output file to.')

    upcoming_events = subparsers.add_parser('upcoming-events',
                                  description='Print upcoming events.')
    upcoming_events.add_argument('config', type=str, help='System path to config file')
    upcoming_events.add_argument('-d', '--date',
                                 default=datetime.now().strftime("%Y%m%d"),
                                 help='Date to use as start point, formatted as YYYYMMDD. Defaults to system date.')
    upcoming_events.add_argument('-t', '--time',
                                 default=datetime.now().strftime("%H%M"),
                                 help='Time to use as start point, formatted as HHMM. Defaults to system time.')
    upcoming_events.add_argument('-n',
                                 default=float("inf"),
                                 type=int,
                                 help='Number of events to display. Displays all events by default.')


    reset = subparsers.add_parser('reset',
                                  description='Set lights to default state.')
    reset.add_argument('config', type=str, help='System path to config file')
    reset.add_argument('-d', '--date',
                       default=datetime.now().strftime("%Y%m%d"),
                       help='Date to use when calculating state, formatted as YYYYMMDD. Defaults to system date.')
    reset.add_argument('-t', '--time',
                       default=datetime.now().strftime("%H%M"),
                       help='Time to use when calculating state, formatted as HHMM. Defaults to system time.')

    turn = subparsers.add_parser('turn',
                              description='Change the state of a specific light.')
    turn.add_argument('lightID', type=int, help='Light identifier, an integer >= 0.')
    turn.add_argument('state', type=str, help='State to change to: \'on\' or \'off\'.')
    turn.add_argument('config', type=str, help='System path to config file.')

    refresh = subparsers.add_parser('refresh',
                              description='Send signals to apply the last state used to all lights. Lights that were turned off will be told to turn off, and vise versa.')
    refresh.add_argument('config', type=str, help='System path to config file.')

    set_art = subparsers.add_parser('set-art',
                                    description='Set ASCII art of room layout. The art can contain light id\'s 0-9, that will be colorized to indicate state when the art command is used.')
    set_art.add_argument('art', type=str, help='System path to file containing ASCII art.')
    set_art.add_argument('config', type=str, help='System path to config file.')

    art = subparsers.add_parser('art',
                                description='Print room layout ASCII art')
    art.add_argument('config', type=str, help='System path to config file.')



    args = parser.parse_args()

    if args.command == 'genconfig':
        do_genconfig(args.output_path)
    if args.command == 'upcoming-events':
        do_upcoming_events(args.config, args.date, args.time, args.n)
    if args.command == 'reset':
        do_reset(args.config, args.date, args.time)
    if args.command == 'turn':
        do_turn(args.config, args.lightID, args.state)
    if args.command == 'set-art':
        do_set_art(args.config, args.art)
    if args.command == 'art':
        do_art(args.config)

if __name__ == '__main__':
    main()
