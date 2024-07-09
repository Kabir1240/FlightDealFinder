import json
import smtplib as smtp
from flight_search import FlightSearch
from data_manager import DataManager
from datetime import datetime, timedelta
from typing import Dict


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.data_manager = DataManager()
        self.flight_search = FlightSearch()

    def get_cheap_flights(self, days:int=186, city_data:list|None=None) -> list:
        if city_data is None:
            city_data = self.data_manager.get_flight_data()

        cheap_flights = []
        for n_days in range(1, days+1):
            date = (datetime.now() + timedelta(days=n_days)).strftime('%Y-%m-%d')
            for city in city_data:
                print(f"Searching for flights to {city["city"]} on {date}")
                flight_data = self.flight_search.get_flight_offers(destination_code=city["iataCode"], date=date)
                if flight_data is not None:
                    for flight in flight_data:
                            if city['lowestPrice'] is None or (flight['price'] <= city['lowestPrice']):
                                cheap_flights.append(flight)
                                city['lowestPrice'] = flight['price']

        for city in city_data:
            self.data_manager.update_lowest_price(row_number=city['id'], lowest_price=city['lowestPrice'])

        return(cheap_flights)


    def get_email_and_password(self) -> Dict:
        """
        retrieves data from EMAIL_PATH and returns it
        :return: dictionary containing name, email and password
        """

        with open(self.email_path, "r") as file:
            data = json.load(file)

        return data


    def send_email(self, from_email, from_pass, to_email, message_body) -> None:
        """
        sends email from one account to another
        :return: None
        """
        with smtp.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=from_email, password=from_pass)
            connection.sendmail(
                from_addr=from_email,
                to_addrs=to_email,
                msg=f"subject:Cheap Flight Found!\n\n{message_body}")
            

    def email_cheap_flights(self):
        cheap_flights = self.get_cheap_flights()

        from_data = self.get_email_and_password
        user_data = self.data_manager.get_user_data()

        for flight in cheap_flights:
            for user in user_data:
                mmessage_body = f"Hey {user['firstName']}{user['lastName']}!\nCatch a flight going to {flight['destination']} 
                on {flight['date']} for just {flight['price']}!"

                self.send_email(from_email=from_data['email'], from_pass=from_data['password'], 
                                to_email=user['email'], message_body=mmessage_body)
