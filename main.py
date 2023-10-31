# Main for Gateway Side AlLoRa
# HW: Raspberry Pi + TTGO Adapter

import  sys, os

from AlLoRa.Nodes.Gateway import Gateway
from AlLoRa.Connectors.Serial_connector import Serial_connector

serial_path = os.eviron.get('SERIAL_PATH', '/dev/ttyAMA3')
volume_path = os.eviron.get('ALLORA_FILES')

if __name__ == "__main__":
	connector = Serial_connector(serial_port = serial_path, baud= '9600', timeout=1)
	allora_gateway = Gateway(connector, config_file= "LoRa.json", debug_hops= False, TIME_PER_ENDPOINT=10)

	# Listen to the digital_endpoints and print and save the files as they come in
	allora_gateway.check_digital_endpoints(print_file_content = True, save_files = True)
	
	
