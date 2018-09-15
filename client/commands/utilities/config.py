import csv

class LightInformation:
    def __init__(self, host, port, light_id):
        self.hostname = host
        self.port = port
        self.light_id = light_id

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
            light = int(e[2])
            if light not in self.state:
                self.state[light] = False

    def light_info(self, light_id):
        entry = None
        for e in self.server_data:
            if int(e[2]) == light_id:
                entry = e
                break
        if entry is None:
            return None
        return LightInformation(host=e[0], port=int(e[1]), light_id=e[2])


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
