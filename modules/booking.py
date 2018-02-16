"""
Attributes:
    API_booking (str): Booking address API
"""
import datetime
import logging
import requests


import modules.search_flights as search_flights

API_booking = 'http://128.199.48.38:8080/booking'

class BookFlight():

	"""Class that makes a booking request based of a given API
	
	Attributes:
	    bags (int): Number of bags included
	    email (TYPE): Description
	    flight_token (TYPE): Description
	    name (str): First name
	    surname (str): Second name
	    title (TYPE): Mr or Mrs
	
	Deleted Attributes:
	    flight (str): Booking token for a given flight
	"""
	
	def __init__(self, flight_token:str, name:str = 'Michal', surname:str = 'Kucirka', 
	email:str = 'michal.kucirka@gmail.com', title:str = 'Mr', bags:int = 0 ):
		self.flight_token = flight_token
		self.name = name
		self.surname = surname
		self.email = email
		self.title = title
		self.bags = bags
		self.logger = logging.getLogger('Booking')

	def create_payload(self) -> dict:
		"""Creates a payload of parameters that is later parse into booking request
		
		Returns:
		    dict: payload of booking parameters
		"""
		payload = {
		'bags' : self.bags,
		'currency' : 'EUR',
		'passengers': 
		{
	        "firstName": self.name,
	        "lastName": self.surname,
	        "title": 'Mr',
	        "email": self.email,
	        'documentID': '123456789',
	        'birthday' : '1993-03-03'
	      }
		,
	    'booking_token': self.flight_token,
		}
		return payload	

	def booking_request(self) -> requests:
		"""Creates a post request to the Kiwi API and makes a booking
		
		Returns:
		    requests: Description
		"""
		payload = self.create_payload()
		try:
			booking_request = requests.post(API_booking , json = payload)
			return booking_request
		except requests.exceptions.RequestException as e:
			print (e)
			sys.exit(1) 

	def get_confirmation_number(self) -> str:
		"""Method that calls booking request and returns confirmation number if booking
		is succesfull
		
		Returns:
		    str: confirmation number of a booking
		"""
		booking_request = self.booking_request()
		if booking_request.status_code != 200:
			self.logger.error('Request failed:'.format(booking_request.content))
		else:
			return booking_request.json()['pnr']



