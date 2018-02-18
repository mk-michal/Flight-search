#!/usr/bin/env python3
"""Module, that initiate program via command line

Attributes:
    API_SKYPICKER (str): Kiwi API for making request
"""
import datetime
import logging
import os
import requests


import click


from modules import FlightInfo, BookFlight, LoggingHandler


API_SKYPICKER = 'https://api.skypicker.com/'

logger = LoggingHandler().log 

def get_location_payload(location: str, language:str = 'en-US') -> dict:
	"""Makes a location payload in order to parse it onto location get request
	
	Args:
	    location (str):Given three - letter AITI airport code
	    language (str, optional): language of the output
	
	Returns:
	    dict: payload with parameters to location request
	"""
	return {
		'type': 'id',	
		'id' : location,
		'locale' : language
	}

def validate_date(ctx, param, value):
	"""Function that validates if the given date is in correct format (%Y-%m-%-d)
	and changes format to %d/%m/%Y in order to parse it onto search_flight module
	
	Args:
	    param (str): date in format (%Y-%m-%-d)
	
	Returns:
	    str: date in format %d/%m/%Y 	
	"""
	try:
		date = datetime.datetime.strptime(value, '%Y-%m-%d').strftime('%d/%m/%Y')
		return date
	except ValueError:
		raise click.BadParameter("Incorrect format, datetime format should match %Y-%m-%d")


def make_location_request(location:str):

	payload = get_location_payload(location)
	try:
		location_request = requests.get(os.path.join(API_SKYPICKER, 'locations'), params = payload)
		return location_request
	except requests.exceptions.RequestException as e:
		print (e)
		sys.exit(1)


def validate_departure_airport(ctx, param, value):
	"""Function that validates if the given airport exists and if it is in the correct format 
	
	Args:
	    param (TYPE): Three - letter airport IATA code
	
	Returns:
	    str: Three - letter airport IATA code	
	"""
	location_request = make_location_request(value) 
	if location_request.status_code != 200:
		logger.error(
			'Request failed while requesting arrival airrport:Error {}'. format(location_request.status_code)
			)
	else:
		location_info = location_request.json()['locations']
		if location_info and location_info[0]['code'] == value:
			return value
		else:
			raise click.BadParameter(
				'Given departure airport does not match any IATA code'
				)


def validate_arrival_airport(ctx, param, value):
	"""Function that validates if the given arrival airport exists and if it is in the 
	correct format.  

	
	Args:
	    param (str): Three - letter airport IATA code
	
	Returns:
	    str: Three - letter airport IATA code
	
	"""
	location_request = make_location_request(value) 

	if location_request.status_code != 200:
		logger.error(
			'Request failed while requesting arrival airrport: Error {}'. format(location_request.status_code)
			)
	else:
		location_info = location_request.json()['locations']
		if location_info and location_info[0]['code'] == value:
			return value
		else:
			raise click.BadParameter(
				'Given departure airport does not match any IATA code'
				)


@click.command()
@click.option('--date', callback = validate_date, help = 'Date of departure in formay YYYY-mm-dd', type = str)
@click.option('--from','departure',callback = validate_departure_airport,
 help = 'IATA code of departure airport', type = str)
@click.option('--to', callback = validate_arrival_airport,
 help = 'IATA code of arrival airport', type = str)
@click.option('--bags', default = 0, help = 'Number of bags', type = int)
@click.option('--return','nights_to_stay', default = None, help = 'Number of nights for one stay', type = int)
@click.option('--cheapest', is_flag = True, default = True, help = 'Find the cheapest flight', type = bool)
@click.option('--fastest', is_flag = True,  help = 'Find the fastest flight', type = bool)
@click.option('--one-way','one_way', is_flag = True, default = True, help = 'Search only one-way flights', type = bool)



def make_booking(date:str, departure:str, to:str, bags:int, nights_to_stay:int,
cheapest:bool, fastest:bool, one_way:bool) -> str:
	"""Function finds flight based on given parameters in Flight_info class and if the 
	flight exists, than makes a booking via Book_flight class.
	
	Args:
	    date (str): date in format (%Y-%m-%-d)
	    departure (str): Three- letter IATA of departure airport
	    to (str): Three- letter IATA code of arrival airport
	    bags (int): Number of bags
	    nights_to_stay (int): Number of nights to stay
	    cheapest (bool): True value returns cheapest flight (Default)
	    fastest (bool): True value returns the fastest flight
	    one_way (bool): True value returns one-way trip, False returns round (default = True)
	"""
	one_way = False if nights_to_stay else True
	if fastest:
		flight = FlightInfo(
			departure, to, date, one_way = one_way, nights_to_stay = nights_to_stay
			).pick_fastest_flight()
	else:
		flight = FlightInfo(
			departure, to, date, one_way = one_way, nights_to_stay = nights_to_stay
			).pick_cheapest_flight()

	confirmation_number = BookFlight(flight['booking_token'], bags = bags).get_confirmation_number()
	
	return click.echo('Reservation number is {}'.format(confirmation_number))

if __name__ == '__main__':
	make_booking()










