import datetime
import os
import requests


import click

from modules import search_flights, booking


API_skypicker = 'https://api.skypicker.com/' 

def validate_date(ctx, param, value):
	try:
		date = datetime.datetime.strptime(value, '%Y-%m-%d').strftime('%d/%m/%Y')
		return date
	except ValueError:
		raise click.BadParameter("Incorrect format, datetime format should match %Y-%m-%d")


def validate_departure_airport():
	payload = {
		'code' : 'YXU'
	}

	headers = {
	'Content-Type':'application/json'

	}
	return requests.get(os.path.join(API_skypicker, 'locations'), headers = headers, data = payload)



@click.command()
@click.option('--date', callback = validate_date, help = 'Date of departure in formay YYYY-mm-dd', type = str)
@click.option('--from','departure', help = 'IATA code of departure airport', type = str)
@click.option('--to', help = 'IATA code of arrival airport', type = str)
@click.option('--bags', default = 0, help = 'Number of bags', type = int)
@click.option('--return','nights_to_stay', default = None, help = 'Number of nights for one stay', type = int)
@click.option('--cheapest', is_flag = True, default = True, help = 'Find the cheapest flight', type = bool)
@click.option('--fastest', is_flag = True,  help = 'Find the fastest flight', type = bool)
@click.option('--one_way', is_flag = True, default = True, help = 'Search only one-way flights', type = bool)

def make_booking(date, departure, to, bags, nights_to_stay, cheapest, fastest, one_way):
	one_way = False if nights_to_stay else True
	cheapest = False if fastest else True
	print(date)

	flight = search_flights.Flight_info(
		departure, to, date, cheapest = cheapest, one_way = one_way, nights_to_stay = nights_to_stay
		).pick_flight()
	booking_request = booking.book_flight(flight, bags = bags).json()

	click.echo('Reservation number is {}'.format(booking_request['pnr']))

if __name__ == '__main__':
	make_booking()










