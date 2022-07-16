# Grocer.io

This project consists of three main elements: the hardware, consisting of a a
Raspberry Pi and a USB barcode scanner in a housing; the website, where users will
configure their account and view/edit their cart; and the server API call to Instacart’s
delivery service, which is how we will place the orders and execute deliveries and
pickups. <br>
<br>
When the user sets up their account via our website, they will input their contact
information, including email and phone number, their address, preferred grocery stores,
the day of the week and time they want the orders to take place, and the payment method.
We will then ship them our hardware for free, and once they receive it, they will pair their
device with their account using a button on the device and website. <br>
<br>
Pairing is achieved by utilizing the fact that the Raspberry Pi and the user’s device
they are using to access the Grocer.io website is on the same internet, which means that
any requests sent to the server from either the Raspberry Pi or the browser will be coming
from the same IP address. We will leverage this to link the Raspberry Pi and the user
account, and we will store the user’s ID (coming from the users table in the database) on
a file locally on the Raspberry Pi. <br>
<br>
Once paired, whenever the user scans an items barcode, the item will be added to
their cart on our server. When the current time matches the day of the week and time the
user selected for their preferred order time, the server will find all local stores and match
any of them to the preferred grocery store specified by the user, and then make an order
using the cart, all of which is done through the Instacart Connect Fulfillment API.