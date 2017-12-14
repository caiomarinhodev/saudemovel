import requests


def geocode(street):
    key = "AIzaSyCn8DVSybps_Qx8EeFz47d2O-QbxJhDeFI"
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (street, key)
    print(url)
    response = requests.get(url)
    print(response.json())
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
            "formatted_address": answer.get('formatted_address'),
            "latitude": answer.get('geometry').get('location').get('lat'),
            "longitude": answer.get('geometry').get('location').get('lng'),
            "accuracy": answer.get('geometry').get('location_type'),
            "google_place_id": answer.get("place_id"),
            "type": ",".join(answer.get('types')),
            "postcode": ",".join([x['long_name'] for x in answer.get('address_components')
                                  if 'postal_code' in x.get('types')])
        }
    print(output)
