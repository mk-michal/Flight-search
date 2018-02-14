import datetime
import requests
import json
import os
from urllib.parse import urljoin

API_skypicker = 'https://api.skypicker.com/' 

class Flight_info():
	def __init__(self, departure_airport: str, arrival_airport: str, departure_date: str, 
	cheapest = True, one_way = True, nights_to_stay: int = None):
		self.departure_airport = departure_airport
		self.arrival_airport = arrival_airport
		self.departure_date = departure_date
		self.cheapest = cheapest
		self.one_way = one_way
		self.nights_to_stay = nights_to_stay
		self.payload = self.create_payload()

	def create_payload(self):
		payload = {
		    'flyFrom': self.departure_airport,
		    'to' : self.arrival_airport,
		    'locale': 'en-US',
		    'dateFrom' : self.departure_date,
		    'dateTo'  : self.departure_date,
		    'typeFlight' : 'oneway' if self.one_way else 'round',
		    'curr' : 'EUR',
		    'daysInDestinationFrom': self.nights_to_stay,
		    'daysInDestinationTo' : self.nights_to_stay,
		    'sort' : 'price' if self.cheapest else 'duration'

		}
		return payload

	def request_flights(self):
		return requests.get(os.path.join(API_skypicker, 'flights'), params = self.payload)

	def pick_flight(self):
		flights = self.request_flights().json()
		print(flights)
		chosen_flight = flights['data'][0]
		return chosen_flight
	


