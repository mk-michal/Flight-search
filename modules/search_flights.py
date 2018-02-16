"""Summary

Attributes:
    API_skypicker (str): Description
"""
import datetime
import requests
import json
import logging
import os
import sys
from urllib.parse import urljoin

API_skypicker = 'https://api.skypicker.com/' 

class FlightInfo():

	"""Class that finds different flight options based on costumer preferences.
	
	Attributes:
	    arrival_airport (str): IATA code of particular arrival airport
	    cheapest (TYPE): Description
	    departure_airport (str): IATA code of particular arrival airport (PRG for Prague)
	    departure_date (str): departure date in format of %d/%m/%Y
	    nights_to_stay (int): nights to stay in the destination
	    one_way (bool): True value if one-way trip, for return False
	"""
	
	def __init__(self, departure_airport: str, arrival_airport: str, departure_date: str, 
	one_way = True, nights_to_stay: int = None):
		self.departure_airport = departure_airport
		self.arrival_airport = arrival_airport
		self.departure_date = departure_date
		self.one_way = one_way
		self.nights_to_stay = nights_to_stay
		self.logger = logging.getLogger('Flight search')

	def create_payload(self, cheapest = True) -> dict:
		"""Method that creates payload based on type of flight, preferences
		
		Returns:
		    dict: payload of parameter to parse into request API
		
		Args:
		    chapest (bool, optional): if equals True, method finds cheapest flight
		    	otherwise finds the fastest flight
		"""
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
		    'sort' : 'price' if cheapest else 'duration'
		}
		return payload

	def request_flights(self, cheapest = True):
		"""Method that returns a request to Kiwi API
		
		Returns:
		    request: Kiwi API request
		
		Args:
		    payload (dict): payload parameters to add into request
		"""

		payload = self.create_payload(cheapest)
		try:
			flight_request = requests.get(
				os.path.join(API_skypicker, 'flights'), params = payload
				)
			return flight_request
		except requests.exceptions.RequestException as e:
			sys.exit(1) 

	def pick_cheapest_flight(self) -> dict:
		"""Method that picks cheapest flight
		
		Returns:
		    dict: dictionary of cheapest flight description
		"""
		flights_request = self.request_flights()
		if flights_request.status_code != 200:
			print ('Request failed: Error {}'. format(flights_request.status_code))
		elif not flights_request.json()['data']:
			print ('No flights were found that match given parameters')
		else:
			return flights_request.json()['data'][0]



	def pick_fastest_flight(self):
		"""Method that picks the fastest flight
		
		Returns:
		    dict: dictionary of fastest flight description
		"""
		flights_request = self.request_flights(cheapest = False)
		if flights_request.status_code != 200:
			self.logger.error('Request failed: Error {}'. format(flights_request.status_code))
		elif not flights_request.json()['data']:
			self.logger.info('No flights were found based on given parameters')
		else:
			return flights_request.json()['data'][0]

		


