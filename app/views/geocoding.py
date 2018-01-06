import requests


def calculate_matrix_distance(origin, destination):
    key = " AIzaSyBJZP7dFkC1lguafSNT0E_7rOIzvX03D5U"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=%s&destinations=%s&key=%s" % (
    origin, destination, key)
    response = requests.get(url)
    response = response.json()
    print(response)
    if len(response['rows']) == 0:
        output = {
            "duration": None,
            "dur_value": None,
            "distance": None,
            "dis_value": None
        }
    else:
        answer = response['rows'][0]['elements'][0]
        # print(answer)
        output = {
            "duration": answer.get('duration').get('text'),
            "dur_value": answer.get('duration').get('value'),
            "distance": answer.get('distance').get('text'),
            "dis_value": answer.get('distance').get('value')
        }
    return output


def geocode(street):
    key = "AIzaSyCn8DVSybps_Qx8EeFz47d2O-QbxJhDeFI"
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (street, key)
    response = requests.get(url)
    response = response.json()
    if len(response['results']) == 0:
        output = {
            "formatted_address": None,
            "latitude": None,
            "longitude": None,
            "accuracy": None,
            "google_place_id": None,
            "type": None,
            "postcode": None
        }
    else:
        answer = response['results'][0]
        output = {
            "latitude": answer.get('geometry').get('location').get('lat'),
            "longitude": answer.get('geometry').get('location').get('lng'),
        }
    return output
