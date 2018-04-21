from datetime import datetime
from geopy.distance import vincenty
import requests

from mn_metrotransit import Client, NORTH, SOUTH, EAST, WEST
from . import utils


def get_active_stations_func(route, direction, station_coordinate_map):

    def active_station_func():
        client = Client()
        try:
            raw_locations = client.get_vehicle_locations(route)
        except requests.RequestException:
            raw_locations = []
        directed = [l for l in raw_locations if l['Direction'] == direction]
        return [
            _get_closest_station(loc, station_coordinate_map)
            for loc in directed
        ]

    return active_station_func


def _get_closest_station(vehicle_location, station_coordinate_map):
    veh_coord = (
        vehicle_location['VehicleLatitude'],
        vehicle_location['VehicleLongitude']
    )
    distances = [
        (station, vincenty(veh_coord, stat_cord).meters)
        for station, stat_cord in station_coordinate_map.items()
    ]
    station = min(distances, key=lambda x: x[1])
    return station[0]


def get_arrival_func(route, direction, station_id):

    def arrival_func():
        client = Client()
        try:
            raw_arrivals = client.get_timepoint_departures(
                route, direction, station_id
            )
        except requests.RequestException:
            raw_arrivals = []
        return [
            utils.seconds_from_now(arrival['DepartureTime'])
            for arrival in raw_arrivals
        ]

    return arrival_func
