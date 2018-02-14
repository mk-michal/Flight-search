import requests
import datetime
import modules.search_flights as search_flights

API_booking = 'http://128.199.48.38:8080/booking'


def book_flight(flight: dict, name:str = 'Michal', surname:str = 'Kucirka', 
email:str = 'michal.kucirka@gmail.com', title:str = 'Mr', bags:int = 0 ):
	
	print(flight['price'])

	values = {
	'bags' : bags,
	'currency' : 'EUR',
	'passengers': 
	{
        "firstName": name,
        "lastName": surname,
        "title": 'Mr',
        "email": email,
        'documentID': '123456789',
        'birthday' : '1993-03-03'
      }
	,
    'booking_token': flight['booking_token'],
	}


	headers = {'Content-Type': 'application/json'}

	return requests.post(API_booking , json = values, headers = headers)
