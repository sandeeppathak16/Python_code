import requests

class DataManager:
    def __init__(self, key):
        self.sheet_key = key
        self.destination_data = {}

    def get_all_data(self):
        response = requests.get(url=self.sheet_key)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data
    def put_data(self):
        new_key = f"{self.sheet_key}/{id}"
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{self.sheet_key}/{city['id']}",
                json=new_data
            )
            print(response.text)