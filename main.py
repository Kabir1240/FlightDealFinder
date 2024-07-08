import json
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


def get_cheap_flights(months:int=6) -> list:
    with open('flight_dummy_data.json','r') as file:
        city_data = json.load(file)['prices']
    
    # city_data = DATA_MANAGER.get_flight_data()

    days = months*31
    cheap_flights = []
    for n_days in range(days):
        date = (datetime.now() + timedelta(days=n_days)).strftime('%Y-%m-%d')
        for city in city_data:
            print(f"Searching for flights to {city["city"]} on {date}")
            flight_data = FLIGHT_SEARCH.get_flight_offers(destination_code=city["iataCode"], date=date)
            if flight_data is not None:
                for flight in flight_data:
                        print(flight['price'], city['lowestPrice'])
                        if flight['price'] < city['lowestPrice']:
                            cheap_flights.append(flight)


print(get_cheap_flights())

