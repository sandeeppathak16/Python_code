from data_manager import DataManager
from pprint import pprint
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager


SHEET_KEY = "https://api.sheety.co/d53b204dbf855727243a0156e36ba2a4/flightDeals/prices"

my_data_manager = DataManager(SHEET_KEY)

sheet_data = my_data_manager.get_all_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()
ORIGIN_CITY_IATA = "LON"
if sheet_data[0]["iataCode"] == "":
    from flight_search import FlightSearch
    flight_search = FlightSearch()
    for row in sheet_data:
        row["iataCode"] = flight_search.get_iata(row["city"])
    print(f"sheet_data:\n {sheet_data}")
    my_data_manager.destination_data=sheet_data
    my_data_manager.put_data()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

for destination_code in destinations:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination_code,
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight is None:
        continue

    if flight.price < destinations[destination_code]["price"]:
        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."

        ######################
        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            print(message)
        #######################

        notification_manager.send_sms(message)