from .utilities.config import Config

def do(output_path):
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

    def input_location_conf():
        print('-- LOCATION CONFIGURATION --')
        print('Enter:')
        print('>latitude, longitude')
        print('As floats.')
        inp = input('>').replace(' ', '').split(',')
        return [float(e) for e in inp]

    def input_server_conf():
        print('-- SERVER CONFIGURATION --')
        print('Enter the following any number of times. Enter empty line when you\'re done')
        print('> host-address, port, light-id')
        print('    host-adress: Ip address for a lights server')
        print('    port: The port on that server to use for light toggle requests.')
        print('    light-id: The light ID of a light.')
        rslt = []
        while True:
            print('Enter another light...')
            inp = input('>').replace(" ", "").split(',')
            if inp == ['']:
                break
            print(inp)
            rslt.append( (inp[0], int(inp[1]), int(inp[2])) )
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
    valid_light_ids = list(set(e[2] for e in server_conf))
    event_conf = input_event_conf(valid_light_ids)

    conf = Config()
    conf.latitude = location_conf[0]
    conf.longitude = location_conf[1]
    conf.server_data = server_conf
    conf.events = event_conf
    conf.path = output_path
    conf.write()
