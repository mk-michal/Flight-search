# Kiwi flight booking app

The main goal of the project is to create a script that finds and books flight ticket based on given parameters. Skypicker (Kiwi) API was used for flight search and special API for Kiwi python weekend was used for flight booking (the reason is that this API doesn't require any payment and the booking is ). 

API skypicker:
```https://api.skypicker.com/```

API for booking:
```http://128.199.48.38:8080/booking```

Script is initialized via command line in the following manner:

```
 ./book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way
 ./book_flight.py --date 2018-04-13 --from LHR --to DXB --return 5
 ./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2
 ./book_flight.py --date 2018-04-13 --from CPH --to MIA --fastest
```

* --one-way (default option) means one-way trip
* --return 5 means bookin of flight ticket with 5 nights in one particular place
* --cheapest (default option) books the cheapest flight and --fastest books the fastest
* --bags 2 books flight with two bags
* -- from and --to are parameters that requires IATA codes of departure and arrival airports

The output of the program (if done succesfully) is a Booking reservation number.

The main part of the script is written in two main modules `booking.py` and `search_flights.py` in `modules` folder. The app is initialized via `book_flight` module. 
