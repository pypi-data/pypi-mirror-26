# iupick-python

The iupick Python package wraps the iupick API to facilitate access from applications written in python.

Keep in mind that this package requires iupick secret keys, contact
info@iupick.com for more information.

## Installation

Install the package with:

`pip install iupick`

## Waybills

The waybill generation occurs on three steps.

Never expose your secret token.

Methods that require your secret_token should never be done from the front-end. Since this methods deal with sensitive information. 

### Step 1.

Create a shipment on the iuPick platform and receive a
shipment token.

``` python

from iupick import iupick

iupick.secret_token = 'sk_sandbox_c7ad5687da0dc5a7dc4142a6079213ddb4ccfbff'
iupick.environment = 'sandbox'

def create_token():
    return iupick.Shipment.create(length=8,
                                  width=8,
                                  height=8,
                                  weight=1.1)

```

### Step 2.

Fill the rest of the information required to generate a waybill,
and receive a confirmation token.

You can send a shipment either to an arbitrary direction or to one
of our waypoints; just replace the waypoint_id attribute for a recipient
address.

``` python

iupick.public_token = '5c2a15c518845484302b532413e1bc303add53b6'
iupick.environment = 'sandbox'

def fill_shipment_information(shipment_token):

    shipper_address = iupick.create_address(city='Querétaro',
                                            line_one='Epigmenio Gonzáles 500',
                                            postal_code=76130,
                                            line_two='',
                                            neighborhood='Momma')

    shipper_contact = iupick.create_person(person_name='Tony Stark',
                                           phone_number='555555555',
                                           email_address='tony@fakemail.com',
                                           title='CEO',
                                           company_name='Stark Industries',
                                           phone_extension='123')


    recipient_contact = iupick.create_person(person_name='Steve Rogers',
                                             phone_number='555555555',
                                             email_address='steve@fakemail.com',
                                             title='Agent',
                                             company_name='SHIELD',
                                             phone_extension='123')

    return iupick.Shipment.add_information(shipment_token=shipment_token,
                                           waypoint_id=486,
                                           shipper_address=shipper_address,
                                           shipper_contact=shipper_contact,
                                           recipient_contact=recipient_contact,
                                           third_party_reference='I am a shipment')
```

### Step 3.

Generate your waybill with your confirmation token.

``` python

iupick.secret_token = 'sk_sandbox_c7ad5687da0dc5a7dc4142a6079213ddb4ccfbff'
iupick.environment = 'sandbox'

def generate_waybill(confirmation_token):
    return iupick.Shipment.generate_waybill(confirmation_token=confirmation_token)
```

### Tracking your shipment

In order to track a shipment send the carrier and the tracking number.

``` python

iupick.public_token = '5c2a15c518845484302b532413e1bc303add53b6'
iupick.environment = 'sandbox'

def track_shipment(carrier, tracking_number):
    return iupick.Shipment.track(carrier=carrier,
                                 tracking_number=tracking_number)

```

### Waypoints

The Waypoints resource allows you to interact with all the delivery points from
our network that are available to your account.

To pull the full information for a single waypoint. Use `getWaypointInformation`
It requires the waypoint unique id.

``` python

iupick.public_token = '5c2a15c518845484302b532413e1bc303add53b6'
iupick.environment = 'sandbox'

def get_waypoint_information(waypoint_id):
    return iupick.Waypoints.get_waypoint_information(waypoint_id)
```

To get a list of all the coordinates of available waypoints, use
`getWaypointsLite`.

``` python

iupick.public_token = '5c2a15c518845484302b532413e1bc303add53b6'
iupick.environment = 'sandbox'

def get_waypoints_lite():
    return iupick.Waypoints.get_waypoints_lite()
```

You can get all the waypoints close to a Postal Code with
`getPostalCodeWaypoints`.

``` python

iupick.public_token = '5c2a15c518845484302b532413e1bc303add53b6'
iupick.environment = 'sandbox'

def get_postal_waypoints(postal_code):
    return iupick.Waypoints.get_postal_code_waypoints(postal_code)
```