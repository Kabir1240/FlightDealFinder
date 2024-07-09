import json
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager


# global variables
DATA_MANAGER = None
FLIGHT_SEARCH = None
NOTIFICATION_MANAGER = NotificationManager()
EMAIL_PATH = "email.json"

def update_iata_codes() -> None:
    """
    Updates IATA codes for each city in the google sheet document
    """
    sheet_data = DATA_MANAGER.get_flight_data()['prices']

    for city in sheet_data:
        iata_code = FLIGHT_SEARCH.get_iata_code(city['city'])
        DATA_MANAGER.update_iata_code(row_number=city['id'], iata_code=iata_code)


def update_lowest_price() -> None:
    """
    Gets intial lowest prices for each city.
    """
    city_data = DATA_MANAGER.get_flight_data()
    
    for city in city_data:
        city['lowestPrice'] = None
    
    NOTIFICATION_MANAGER.get_cheap_flights(city_data=city_data)


def main():
    """
    Initializes the required data in google sheets and then sends emails to user if cheap flights are found within the next 6 months.
    """
    global DATA_MANAGER
    global FLIGHT_SEARCH

    with open('data.json') as file:
        data = json.load(file)
    
    # check if this is the first time running the application
    if data['data']['FIRST_TIME'] == 'yes':
        # initalize data manager and flight search global variables
        DATA_MANAGER = DataManager()
        FLIGHT_SEARCH = FlightSearch()

        # update IATA codes and lowest prices
        update_iata_codes()
        update_lowest_price()

        # make sure this process only runs once.
        data['data']['FIRST_TIME'] = 'no'
        json.dump(data, 'data.json')

    # find cheap flights and send emails.
    NOTIFICATION_MANAGER.email_cheap_flights()

