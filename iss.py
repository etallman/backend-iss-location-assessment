#!/usr/bin/env python

__author__ = 'Eileen'

import sys
import requests
import turtle
import time


def curr_astro_data(url):
    '''Uses a public API to display a list of details about the astronauts who are currently in space, including the full names and their spacecraft. Also displays the total number of astronauts in space.'''

    r = requests.get(url).json()
    print('\n''---------Current Astronaut Data---------''\n')
    for key in r:
        if key == 'number':
            print('Total Number of Astronauts in Space: {}''\n'.format(str(r[key])))
        if key == 'people':
            print('Astronaut Name: || Spacecraft:')
            for value in r[key]:
                print('{}  ||  {}'.format(value['name'], value['craft']))


def curr_coord_data(url):
    '''Uses a public API to obtain the current geographic coordinates (lat/lon) of the space station, along with a timestamp.'''
    r = requests.get(url).json()
    iss_coords = None

    print('\n''---------ISS Location Data---------''\n')
    for key, value in r.items():
        if key == 'timestamp':
            print('Timestamp: {}''\n'.format(r[key]))
        if key == 'iss_position':
            iss_coords = value
            print('Latitude: || Longitude:')
            print('{} || {}'.format(value['latitude'],value['longitude']))
    return iss_coords
    
    
def overhead_indy(url, iss_coords):
    indy_lat = iss_coords['latitude']
    indy_long = iss_coords['longitude']
    
    url = url +'?lat=' + str(indy_lat) + '&lon=' + str(indy_long)
    r = requests.get(url).json()
    indy_overhead_time = r['response'][1]['risetime']
    indy_overhead_time = time.ctime(indy_overhead_time)
    return indy_overhead_time
    

def turtle_map(iss_coords, indy_overhead_time):
    iss_lat = float(iss_coords['latitude'])
    iss_long = float(iss_coords['longitude'])
    
    #Creating the map
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.bgpic('map.gif')
    screen.setworldcoordinates(-180, -90, 180, 90)
   
    #Plotting ISSfrom curr_coord_data. Longitude given first for xy coords.
    screen.register_shape('iss.gif')
    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.setheading(90)
    iss.penup()
    
   
    #Plot location from overhead_indy
    iss.setposition(iss_long, iss_lat)
    iss.color('white') 
    iss.dot(12, "white")
    iss.write(indy_overhead_time, align='right', font=('Arial', 12, 'bold'))
    iss.goto(iss_long, iss_lat)
    iss.penup()
    
    turtle.done()
    screen.exitonclick()
    
    
def main():
    print(curr_astro_data("http://api.open-notify.org/astros.json"))
    curr_coord_data("http://api.open-notify.org/iss-now.json")
    
    iss_coords = curr_coord_data("http://api.open-notify.org/iss-now.json")
    indy_overhead_time = overhead_indy('http://api.open-notify.org/iss-pass.json', iss_coords)
    
    turtle_map(iss_coords, indy_overhead_time)
    
if __name__ == '__main__':
    main()