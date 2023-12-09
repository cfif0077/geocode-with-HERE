import time
from here_location_services import LS
import csv
from config import API_KEYS, HEADERS, CITY, CLOCK, PATH_IN_FILE, PATH_OUT_FILE

headers = HEADERS
clock = CLOCK
list_api = API_KEYS


def free_geocode(list_api_key, search_address):
    try:
        ls = LS(api_key=list_api_key[-1])
    except IndexError:
        print('ключи закончились')
    try:
        gc_response = ls.geocode(query=search_address)
        geodata = gc_response.to_geojson()
        try:
            geodata = geodata['features'][0]['geometry']['coordinates']
            lines.append(geodata[0])
            lines.append(geodata[1])
            print(lines)
            return lines
        except IndexError:
            print(search_address, geodata)
            return search_address, geodata
    except Exception as inst:
        print(inst)
        ex = str(inst)[:3]
        match ex:
            case '429':
                list_api_key.pop()
                return free_geocode(list_api_key, search_address)
            case '504':
                time.sleep(1)
                return free_geocode(list_api_key, search_address)


with open(PATH_IN_FILE, mode='r') as file, open(PATH_OUT_FILE, mode='a', newline='') as file1:
    csvFile = csv.reader(file)
    write = csv.DictWriter(file1, fieldnames=headers)
    for lines in csvFile:
        if lines[3] == 'location':
            print(headers)
            if clock == '0':
                write.writeheader()
        else:
            if int(lines[0]) > int(clock):
                clock = lines[0]
                address = lines[3] + CITY
                lines = free_geocode(list_api, address)
                if len(lines) == 2:
                    print(lines)
                else:
                    write.writerow(dict(zip(headers, lines)))
