import json
import requests


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        with open("data.json", 'r') as file:
            keys = json.load(file)['keys']

        self.sheety_url = keys['SHEETY_URL']
        self.sheety_token = keys['SHEETY_TOKEN']
    
    def get_flight_data(self):
        # headers
        headers = \
            {
                'Authorization':self.sheety_token,
                'Content-Type':"application/json"
            }
        
        response = requests.get(url=self.sheety_url, headers=headers)
        response.raise_for_status()
        data = response.json()['prices']

        for index in range(len(data)):
            data[index]['lowestPrice'] = float(data[index]['lowestPrice'])
        
        return data
    
    def get_user_data(self):
        # headers
        headers = \
            {
                'Authorization':self.sheety_token,
                'Content-Type':"application/json"
            }
        
        response = requests.get(url=self.sheety_url, headers=headers)
        response.raise_for_status()
        data = response.json()['users']
        
        return data
    
    def update_flight_data(self, row_number:int, city:str, iata_code:str, lowest_price:float) -> None:
        # headers
        headers = \
            {
                'Authorization':self.sheety_token,
                'Content-Type':"application/json"
            }

        payload = \
            {
                'price': \
                    {
                        'city':city,
                        'iataCode':iata_code,
                        'lowestPrice':f"{lowest_price}"
                    }
            }
        
        response = requests.put(url=self.sheety_url+f"/{row_number}", json=payload, headers=headers)
        response.raise_for_status()
        print(f"Updated data for {city}")
    
    def update_iata_code(self, row_number:int, iata_code:str):
        # headers
        headers = \
            {
                'Authorization':self.sheety_token,
                'Content-Type':"application/json"
            }

        payload = \
            {
                'price': \
                    {
                        'iataCode':iata_code,
                    }
            }
        
        response = requests.put(url=self.sheety_url+f"/{row_number}", json=payload, headers=headers)
        response.raise_for_status()
        print(f"Updated data for row number {row_number}")
    
    def update_lowest_price(self, row_number:int, lowest_price:str):
        # headers
        headers = \
            {
                'Authorization':self.sheety_token,
                'Content-Type':"application/json"
            }

        payload = \
            {
                'price': \
                    {
                        'lowestPrice':lowest_price,
                    }
            }
        
        response = requests.put(url=self.sheety_url+f"/{row_number}", json=payload, headers=headers)
        response.raise_for_status()
        print(f"Updated data for row number {row_number}")