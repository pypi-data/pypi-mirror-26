import os
import json
import logging
import random
import socket
import requests
from geopy.distance import vincenty

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

from spade.AID import aid

logger = logging.getLogger()

REGISTER_PROTOCOL = "REGISTER"
CREATE_PROTOCOL = "CREATE"
REQUEST_PROTOCOL = "REQUEST"
TRAVEL_PROTOCOL = "INFORM"

REQUEST_PERFORMATIVE = "request"
ACCEPT_PERFORMATIVE = "accept"
REFUSE_PERFORMATIVE = "refuse"
PROPOSE_PERFORMATIVE = "propose"
CANCEL_PERFORMATIVE = "cancel"
INFORM_PERFORMATIVE = "inform"

TAXI_WAITING = 10
TAXI_MOVING_TO_PASSENGER = 11
TAXI_IN_PASSENGER_PLACE = 12
TAXI_MOVING_TO_DESTINY = 13
TAXI_WAITING_FOR_APPROVAL = 14

PASSENGER_WAITING = 20
PASSENGER_IN_TAXI = 21
PASSENGER_IN_DEST = 22
PASSENGER_LOCATION = 23
PASSENGER_ASSIGNED = 24


def build_aid(agent_id):
    return aid(name=agent_id + "@127.0.0.1", addresses=["xmpp://" + agent_id + "@127.0.0.1"])


coordinator_aid = build_aid("coordinator")


def random_position():
    path = os.path.dirname(__file__) + os.sep + "templates" + os.sep + "data" + os.sep + "taxi_stations.json"
    with open(path) as f:
        stations = json.load(f)["features"]
        pos = random.choice(stations)
        coords = [pos["geometry"]["coordinates"][1], pos["geometry"]["coordinates"][0]]
        lat = float("{0:.6f}".format(coords[0]))
        lng = float("{0:.6f}".format(coords[1]))
        return [lat, lng]


def are_close(coord1, coord2, tolerance=10):
    return vincenty(coord1, coord2).meters < tolerance


def unused_port(hostname):
    """Return a port that is unused on the current host."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((hostname, 0))
    port = s.getsockname()[1]
    s.close()
    return port


def request_path(ori, dest):
    if ori[0] == dest[0] and ori[1] == dest[1]:
        return [[ori[1], ori[0]]], 0, 0
    try:
        url = "http://osrm.gti-ia.upv.es/route/v1/car/{src1},{src2};{dest1},{dest2}?geometries=geojson&overview=full"
        src1, src2, dest1, dest2 = ori[1], ori[0], dest[1], dest[0]
        url = url.format(src1=src1, src2=src2, dest1=dest1, dest2=dest2)
        result = requests.get(url)
        result = json.loads(result.content)
        path = result["routes"][0]["geometry"]["coordinates"]
        path = [[point[1], point[0]] for point in path]
        duration = result["routes"][0]["duration"]
        distance = result["routes"][0]["distance"]
        return path, distance, duration
    except Exception as e:
        logger.error("Error requesting route: {}".format(e))
    return None, None, None


def load_class(class_path):
    module_path, class_name = class_path.rsplit(".", 1)
    mod = __import__(module_path, fromlist=[class_name])
    return getattr(mod, class_name)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator
