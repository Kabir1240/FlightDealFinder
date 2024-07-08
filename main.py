from flight_search import FlightSearch
from data_manager import DataManager
from datetime import datetime, timedelta


DATA_MANAGER = DataManager()
FLIGHT_SEARCH = FlightSearch()

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
def update_iata_codes():
    sheet_data = DATA_MANAGER.get_flight_data()['prices']

    for city in sheet_data:
        iata_code = FLIGHT_SEARCH.get_iata_code(city['city'])
        DATA_MANAGER.update_iata_code(row_number=city['id'], iata_code=iata_code)


def get_cheap_flights(months:int=6):
    days = months*31
    for n_days in range(days):
        date = (datetime.now() + timedelta(days=n_days)).strftime('%Y-%m-%d')
        