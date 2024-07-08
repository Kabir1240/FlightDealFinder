import requests
import json


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    
    def __init__(self):
        with open("keys.json", 'r') as file:
            keys = json.load(file)

        self.amadeus_url = "https://test.api.amadeus.com/"
        self.amadeus_city_search_endpoint = "v1/reference-data/locations/cities"
        self.amadeus_auth_endpoint = "v1/security/oauth2/token"
        self.amadeus_flight_offers_endpoint = "v2/shopping/flight-offers"
        self.amadeus_api_key = keys['AMADEUS_API_KEY']
        self.amadeus_api_secret = keys['AMADEUS_API_SECRET']
        self.origin_code = keys["ORIGIN_LOCATION_CODE"]
        self.currency_code = keys["CURRENCY_CODE"]
    
    def get_iata_code(self, city:str) -> str:
        access_token = "Bearer " + self.get_amadeus_access_token()
        headers = \
            {
                'accept':'application/vnd.amadeus+json',
                'Authorization':access_token,
            }

        params = \
            {
                'keyword':city,
                'max':1,
            }
        
        response = requests.get(url=self.amadeus_url+self.amadeus_city_search_endpoint, headers=headers, params=params)
        response.raise_for_status()
        print(f"Retrieved IATA code for {city}")
        return response.json()['data'][0]['iataCode']

    def get_amadeus_access_token(self) -> str:
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        params = \
            {
                'grant_type': 'client_credentials',
                "client_id":self.amadeus_api_key,
                "client_secret":self.amadeus_api_secret
            }

        response = requests.post(url=self.amadeus_url+self.amadeus_auth_endpoint, headers=headers, data=params)
        response.raise_for_status()
        return response.json()['access_token']

    def get_flight_offers(self, destination_code:str, date:str):
        access_token = "Bearer " + self.get_amadeus_access_token()
        headers = \
            {
                'accept':'application/vnd.amadeus+json',
                'Authorization':access_token,
            }

        params = \
            {
                'originLocationCode':self.origin_code,
                "destinationLocationCode":destination_code,
                'departureDate':date,
                'adults':1,
                'currencyCode':self.currency_code,
                'max':250,
            }
        
        response = requests.get(self.amadeus_url+self.amadeus_flight_offers_endpoint, headers=headers, params=params)
        response.raise_for_status()

        flight_list = []
        for flight in response.json()['data']:
            new_dictionary = \
                {
                    'origin':self.origin_code,
                    'destination':destination_code,
                    'price':float(flight['price']['total']),
                    'date':date
                }
            flight_list.append(new_dictionary)
        
        if len(flight_list) == 0:
            return None
        else:
            return flight_list
