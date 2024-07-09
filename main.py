from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager


DATA_MANAGER = DataManager()
FLIGHT_SEARCH = FlightSearch()
NOTIFICATION_MANAGER = NotificationManager()
EMAIL_PATH = "email.json"

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
def update_iata_codes():
    sheet_data = DATA_MANAGER.get_flight_data()['prices']

    for city in sheet_data:
        iata_code = FLIGHT_SEARCH.get_iata_code(city['city'])
        DATA_MANAGER.update_iata_code(row_number=city['id'], iata_code=iata_code)

def update_lowest_price():
    city_data = DATA_MANAGER.get_flight_data()
    
    for city in city_data:
        city['lowestPrice'] = None
    
    NOTIFICATION_MANAGER.get_cheap_flights(city_data=city_data)
