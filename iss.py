#!/usr/bin/env python

__author__ = 'Eileen'

import sys
import requests
import turtle
import time


def curr_astro_data(url):
    '''Uses a public API to display a list of details about the astronauts who are currently in space, including the full names and their spacecraft. Also displays the total number of astronauts in space.'''
    
    # url = "http://api.open-notify.org/astros.json"
    r = requests.get(url).json()
    
    # for category in r:
    #     if category == 'number':
    #         print('Total Number of Astronauts in Space: {}'.format(str(r[category])))
    #     if category == 'people':
    #         print('Astronaut Name: || Spacecraft:')
    #         for sub_category in r[category]:
    #             print('{} // {}'.format(sub_category.get('name'), sub_category.get('craft')))
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
    # url = "http://api.open-notify.org/iss-now.json"
    r = requests.get(url).json()
    iss_coords = None
    # for category in r:
    #     if category == 'timestamp':
    #         print('Timestamp: {}'.format(str(r[category])))
    #     if category == 'iss_position':
    #         print('Latitude: || Longitude:')
    #         for sub_category in r[category]:
    #             print('{} // {}'.format(sub_category.get('latitude'), sub_category.get('longitude')))
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
    overhead_time = r['response'][1]['risetime']
    overhead_time = time.ctime(overhead_time)
    return overhead_time
    
    # for key, value in r.items():
    #     if key == 'response':
    #         # overhead_time = r['response'][1]['risetime']
    #         overhead_time = value['risetime']
    #overhead_time = iss_coords.write(time.ctime(overhead_time), font = style)
    
    #         style=('Arial', 12, 'bold')
            # iss_coords['overhead_time'] = iss_coords.write(time.ctime(overhead_time), font = style)
    
def turtle_map(iss_coords, indy_coords):
    iss_lat = iss_coords['latitude']
    iss_long = iss_coords['longitude']
    
    indy_lat = indy_coords['latitude']
    indy_long = indy_coords['longitude']
    
    time_indy = indy_coords['overhead_time']
    
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
    iss.goto(iss_long, iss_lat)
   
    #Plot location from overhead_indy
    iss.write(time_indy, align='right', font=('Arial', 12, 'bold'))
    iss.setposition(indy_long, indy_lat)
    iss.dot(8, "white")
    iss.color("white")
    iss.penup()
    iss.goto(indy_long, indy_lat)
    
    # turtle.done()
    screen.exitonclick()
    
    
def main():
    print(curr_astro_data("http://api.open-notify.org/astros.json"))
    curr_coord_data("http://api.open-notify.org/iss-now.json")
    
    iss_coords = curr_coord_data("http://api.open-notify.org/iss-now.json")
    indy_coords = overhead_indy('http://api.open-notify.org/iss-pass.json', iss_coords)
    
    turtle_map(iss_coords, indy_coords)
    
if __name__ == '__main__':
    main()