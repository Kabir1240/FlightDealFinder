import json
import requests
from typing import Dict


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        """
        set up required user keys
        """

        # get sheety API keys
        with open("data.json", 'r') as file:
            keys = json.load(file)['keys']

        self.sheety_url = keys['SHEETY_URL']
        self.sheety_token = keys['SHEETY_TOKEN']
    
    def get_flight_data(self) -> list[Dict]:
        """
        Retrieve cities, IATA codes and lowest prices from the google sheet doc

        Returns:
            list[Dict]: A list of dictionaries where each dictionary represents one entry.
        """

        # headers
        headers = \
            {
                'Authorization':self.sheety_token,
                'Content-Type':"application/json"
            }
        
        # get response
        response = requests.get(url=self.sheety_url, headers=headers)
        response.raise_for_status()

        # update all prices to float for use.
        data = response.json()['prices']
        for index in range(len(data)):
            data[index]['lowestPrice'] = float(data[index]['lowestPrice'])
        
        # return updated data
        return data
    
    def get_user_data(self) -> list[Dict]:
        """
        retrieves user data from google sheets

        Returns:
            list[Dict]: a list of dictionaries where each dictionary represents a users data.
        """

        # headers
        headers = \
            {
                'Authorization':self.sheety_token,
                'Content-Type':"application/json"
            }
        
        # get response
        response = requests.get(url=self.sheety_url, headers=headers)
        response.raise_for_status()
        data = response.json()['users']
        
        # return data
        return data
    
    def update_flight_data(self, row_number:int, city:str, iata_code:str, lowest_price:float) -> None:
        """
        Update all entries in a row, in the prices google sheet

        Args:
            row_number (int): row to edit
            city (str): name of the city
            iata_code (str): the cities IATA code
            lowest_price (float): lowest price for a flight to that city
        """
        # headers
        headers = \
            {
                'Authorization':self.sheety_token,
                'Content-Type':"application/json"
            }

        # payload
        payload = \
            {
                'price': \
                    {
                        'city':city,
                        'iataCode':iata_code,
                        'lowestPrice':f"{lowest_price}"
                    }
            }
        
        # get response
        response = requests.put(url=self.sheety_url+f"/{row_number}", json=payload, headers=headers)
        response.raise_for_status()
        # inform user
        print(f"Updated data for {city}")
    
    def update_iata_code(self, row_number:int, iata_code:str) -> None:
        """
        update only the IATA code for an entry in the google sheet

        Args:
            row_number (int): row to edit
            iata_code (str): IATA code
        """
        # headers
        headers = \
            {
                'Authorization':self.sheety_token,
                'Content-Type':"application/json"
            }

        # payload
        payload = \
            {
                'price': \
                    {
                        'iataCode':iata_code,
                    }
            }
        
        # get response
        response = requests.put(url=self.sheety_url+f"/{row_number}", json=payload, headers=headers)
        response.raise_for_status()
        # inform user
        print(f"Updated data for row number {row_number}")
    
    def update_lowest_price(self, row_number:int, lowest_price:str) -> None:
        """
        Edit only the lowest price to a city in the google sheet

        Args:
            row_number (int): row to edit
            lowest_price (str): lowest price
        """

        # headers
        headers = \
            {
                'Authorization':self.sheety_token,
                'Content-Type':"application/json"
            }
        
        # payload
        payload = \
            {
                'price': \
                    {
                        'lowestPrice':lowest_price,
                    }
            }
        
        # get response
        response = requests.put(url=self.sheety_url+f"/{row_number}", json=payload, headers=headers)
        response.raise_for_status()
        # inform user
        print(f"Updated data for row number {row_number}")