import requests
import json


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    
    def __init__(self):
        with open("data.json", 'r') as file:
            data = json.load(file)

        # load user keys
        self.amadeus_url = "https://test.api.amadeus.com/"
        self.amadeus_city_search_endpoint = "v1/reference-data/locations/cities"
        self.amadeus_auth_endpoint = "v1/security/oauth2/token"
        self.amadeus_flight_offers_endpoint = "v2/shopping/flight-offers"
        self.amadeus_api_key = data['keys']['AMADEUS_API_KEY']
        self.amadeus_api_secret = data['keys']['AMADEUS_API_SECRET']

        # load user settings
        self.origin_code = data['init_data']["ORIGIN_LOCATION_CODE"]
        self.currency_code = data['init_data']["CURRENCY_CODE"]
    
    def get_iata_code(self, city:str) -> str:
        """
        get the IATA code for a certain city

        Args:
            city (str): name of city

        Returns:
            str: the IATA code
        """

        # headers
        access_token = "Bearer " + self.get_amadeus_access_token()
        headers = \
            {
                'accept':'application/vnd.amadeus+json',
                'Authorization':access_token,
            }

        # parameters
        params = \
            {
                'keyword':city,
                'max':1,
            }

        # get response        
        response = requests.get(url=self.amadeus_url+self.amadeus_city_search_endpoint, headers=headers, params=params)
        response.raise_for_status()

        # inform user
        print(f"Retrieved IATA code for {city}")
        # return the IATA code
        return response.json()['data'][0]['iataCode']

    def get_amadeus_access_token(self) -> str:
        """
        get Amadeus Token for authorization.

        Returns:
            str: token
        """

        # headers
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        # parameters
        params = \
            {
                'grant_type': 'client_credentials',
                "client_id":self.amadeus_api_key,
                "client_secret":self.amadeus_api_secret
            }

        # get response
        response = requests.post(url=self.amadeus_url+self.amadeus_auth_endpoint, headers=headers, data=params)
        response.raise_for_status()
        # return access token
        return response.json()['access_token']

    def get_flight_offers(self, destination_code:str, date:str) -> list:
        """
        get all flight offers for a certain destination

        Args:
            destination_code (str): IATA code for destination
            date (str): date of flight

        Returns:
            list: list of flights
        """

        # headers
        access_token = "Bearer " + self.get_amadeus_access_token()
        headers = \
            {
                'accept':'application/vnd.amadeus+json',
                'Authorization':access_token,
            }

        # params
        params = \
            {
                'originLocationCode':self.origin_code,
                "destinationLocationCode":destination_code,
                'departureDate':date,
                'adults':1,
                'currencyCode':self.currency_code,
                'max':250,
            }
        
        # get response
        response = requests.get(self.amadeus_url+self.amadeus_flight_offers_endpoint, headers=headers, params=params)
        response.raise_for_status()

        # organize return data for a more condensed and readable formm
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
        
        # if no flights are found, return None
        if len(flight_list) == 0:
            return None
        else:
            return flight_list
