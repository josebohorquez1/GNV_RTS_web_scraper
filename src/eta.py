import requests
from bs4 import BeautifulSoup
class ETA(BeautifulSoup):
    def __init__(self, stop_id='----', route_number = '0', direction = 'none', show_all_buses = 'on'):
        self.route_number = route_number
        self.direction = direction
        self.stop_id = stop_id
        self.show_all_buses = show_all_buses
    def find_stops(self):
        stop_names = []
        stop_ids = []
        stops = {}
        i = 0
        url = "https://riderts.app/bustime/wireless/html/selectstop.jsp"
        response = requests.get(url, {'route': self.route_number, 'direction': self.direction.upper()})
        super().__init__(response.content, 'html.parser')
        ul = self.find_all('ul')[1]
        li = ul.find_all('li')
        for a in li:
            links = a.find('a')
            stop_names.append(links.string)
            stop_ids.append(links['href'])
        while i < len(stop_names):
            stop_names[i] = stop_names[i].replace(' \r\n\t\t\t\t', '')
            stop_names[i] = stop_names[i].replace('\r\n\t\t\t', '')
            ids = stop_ids[i].split('id=')
            stop_ids[i] = ids[1][0:4]
            i += 1
        for j in range(len(stop_names)):
            stops.update({stop_names[j]: stop_ids[j]})
        return stops
    def print_stop_list(self):
        stops = self.find_stops()
        print(f'Stops for route {self.route_number}:\n')
        for l in stops:
            print(f'{l}\n')
    def find_stop_id(self, name):
        stops = self.find_stops()
        result = ''
        if name in stops:
            result = stops[name]
            print('found stop')
        else:
            print('could not find stop. Exiting program')
            exit()
        return result
    def set_route_number(self, n):
        self.route_number = str(n)
    def set_stop_id(self, id):
        self.stop_id = id
    def set_direction(self, direction):
        self.direction = direction
    def set_show_all_buses_state(self, s):
        self.show_all_buses = s
    def find_eta(self):
        url = "https://riderts.app/bustime/wireless/html/eta.jsp"
        if self.route_number != '0':     
            queries = {'route': self.route_number, 'direction': self.direction.upper(), 'id': self.stop_id, 'showAllBusses': self.show_all_buses.lower()}
        else:
            queries = {'route': '---', 'direction': '---', 'displaydirection': '---', 'stop': '---', 'findstop': 'on', 'selectedRtpiFeeds': '', 'id': self.stop_id}
        response = requests.get(url, params=queries)
        super().__init__(response.content, 'html.parser')
    def print_eta(self):
        list = []
        i = 0
        stop_string = self.title.string
        stop_string = stop_string.replace('SELECTED STOP | ', '')
        stop_string = stop_string.replace(' - ETA', '')
        stop_string = stop_string.replace('\t', '')
        print(f'Arrival times for stop {stop_string[2:-2]}:')
        for minutes in self.find_all('strong'):
            list.append(minutes.string)
        while i < len(list):
            if (list[i] == 'No service is scheduled for this stop at this time.'):
                print('No service is scheduled for this stop at this time.')
                break
            elif list[i] == 'No arrival times available.':
                print('No arrival times available.')
                break
            elif (i + 1) % 2 == 1:
                    list[i] = list[i].replace('\xa0', '')
            else:
                    list[i] = list[i].replace('\xa0MIN', ' minutes')
                    print(f'Bus {list[i - 1]} will arrive in about {list[i]}.\n')
            i += 1
        