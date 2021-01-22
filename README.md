# berkey-fill-alert
a python application using a raspberry pi zero + CQRobot Ocean Water Contact Sensor to determine when a [big berkey](https://www.usaberkeyfilters.com/products/big-berkey-water-filter/) is filled.  Analytics website built in flask.  This project was developed for submission into the 2021 Cambridge Associates Fedex Day (24 hour hackathon).

## configuration
The repo contains a configuration file "berkey-fill-alert-config.example.json" when running this project this should be moved the parent directory of the project and renamed to "berkey-fill-alert-config.json".  Example: if the project is in /home/pi/berkey-fill-alert the config should be located to /home/pi


### packages installed on Raspberry Pi Zero (raspbian OS)
* ssmtp 
* rpi.gpio
* sqlite3
* ...

### GPIO Sensor configuration
Here is the sensor used: https://www.amazon.com/gp/product/B07ZMGW3QJ/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1
![GPIO Sensor Diagram](https://images-na.ssl-images-amazon.com/images/I/71qAZOYICVL._SL1500_.jpg)

