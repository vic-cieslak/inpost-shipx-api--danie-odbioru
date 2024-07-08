import requests
import json
import base64
from flask import jsonify

# Add your secrets here
ORGANIZATION_ID = '111111'
API_URL = 'https://api-shipx-pl.easypack24.net/v1/organizations/' + ORGANIZATION_ID
BEARER_TOKEN = 'YOUR_BEARER_TOKEN'

# Replace the personal information in the payload with placeholders
def create_shipment(client_contact, client_address, package, content=''):
    print('here!')
    url = f'{API_URL}/shipments'

    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
        'Content-Type': 'application/json'
    }

    print('DATA GOING IN:')
    if client_address['apartmentNumber']:
        numer_domu_mieszkania = client_address['houseNumber'] + ' ' + client_address['apartmentNumber']
    else:
        numer_domu_mieszkania = client_address['houseNumber']

    client_phone = client_contact['phoneNumber'].replace('-', '').strip()

    data = {
        "sender": {
            "first_name": client_contact['imie'],
            "last_name": client_contact['nazwisko'],
            "email": client_contact['emailAddress'],
            "phone": client_phone,
            "address": {
                "street": client_address['street'],
                "building_number": numer_domu_mieszkania,
                "city": client_address['city'],
                "post_code": client_address['postalCode'],
                "country_code": "PL"
            }
        },
        "receiver": {
            "company_name": "Company_Name",
            "email": "receiver@example.com",
            "phone": "123456789",
            "address": {
                "street": "Receiver_Street",
                "building_number": "123",
                "city": "Receiver_City",
                "post_code": "00000",
                "country_code": "PL"
            }
        },
        "parcels": [
            {
                "dimensions": {
                    "length": package['length'],
                    "width": package['width'],
                    "height": package['height'],
                    "unit": "mm"
                },
                "weight": {
                    "amount": package['weight'],
                    "unit": "kg"
                }
            }
        ],
        "service": "inpost_courier_standard",
        "additional_services": [
            "email",
            "sms"
        ],
    }
    print(data)

    if client_contact['companyName'] is not None:
        data['sender']['company_name'] = client_contact['companyName']

    if package['uwagi'] is not None:
        data['reference'] = package['uwagi']

    if content is not None:
        data['comments'] = content

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.json())
    data = response.json()
    if data['status'] == 400:
        if data['details']['parcels'][0]['0']['dimensions'] == ['parcel_is_too_large_or_too_heavy']:
            return jsonify({
                "error": 'error',
                "message": 'Paczka jest za duża albo za ciężka.',
            })
        return jsonify({
            "error": 'error',
            "message": 'Błąd.',
        })

    shippment_id = data['id']

    # ZAMÓW ODBIÓR
    url = f"{API_URL}/dispatch_orders"
    print('dispatch orders')
    data = json.dumps({
        "shipments": [shippment_id],
        "phone": client_phone,
        "email": client_contact['emailAddress'],
        "address": {
            "street": client_address['street'],
            "building_number": numer_domu_mieszkania,
            "city": client_address['city'],
            "post_code": client_address['postalCode'],
            "country_code": "PL"
        }
    })

    response = requests.post(url, headers=headers, data=data)
    i = 0
    while response.status_code == 400:
        print('sending another request')
        response = requests.post(url, headers=headers, data=data)
        i += 1
        if i > 10:
            return jsonify({
                "error": 'error',
                "message": 'Paczka utworzona, ale wystąpił błąd przy pobieraniu etykiety. Prosimy o kontakt telefoniczny.',
            })

    print("Status Code:", response.status_code)
    print("Response:", response.json())

    url = f'{API_URL}/shipments/{shippment_id}/label'
    print(url)
    response = requests.get(url, headers=headers)
    pdf_data = response.content
    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

    return jsonify({
        "pdf": pdf_base64,
        "message": 'guess its ok',
    })


if __name__ == '__main__':
    # Example usage (replace these placeholders with actual values)
    client_contact = {
        'imie': 'John',
        'nazwisko': 'Doe',
        'emailAddress': 'john.doe@example.com',
        'phoneNumber': '123-456-7890',
        'companyName': None  # or 'Some Company'
    }
    client_address = {
        'street': 'Main St',
        'houseNumber': '123',
        'apartmentNumber': '',
        'city': 'Sample City',
        'postalCode': '12345'
    }
    package = {
        'length': 100,
        'width': 50,
        'height': 30,
        'weight': 2,
        'uwagi': 'Handle with care'
    }
    response = create_shipment(client_contact, client_address, package)
    print(response)
