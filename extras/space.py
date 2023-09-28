import requests


def get_astronauts():
    """Get info about astronauts in space."""
    return requests.get("http://api.open-notify.org/astros.json").json()

def get_coords_iss():
    """Get the coordinates of the ISS"""
    data = requests.get("http://api.open-notify.org/iss-now.json").json()
    return data["iss_position"]
