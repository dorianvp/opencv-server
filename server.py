import cv2
import socket
import pickle
import struct
import Linguist
from OCR import ocr_from_frame, OCR
import warnings
warnings.filterwarnings("ignore")

# This is the actual server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8001))
server_socket.listen(10)

received_data = b""
payload_size = struct.calcsize("L")

client_socket, address = server_socket.accept()

# OCR initialization
language = "eng"
ocr = OCR().start()
ocr.set_language(language)
lang_name = Linguist.language_string(language)


while True:
	# Receive and assemble the data until the payload size is reached
	while len(received_data) < payload_size:
		received_data += client_socket.recv(4096)

	# Unpack the packed message size
	packed_msg_size = received_data[:payload_size]
	received_data = received_data[payload_size:]
	msg_size = struct.unpack("L", packed_msg_size)[0]

	# Receive and assemble the frame until the complete frame is received
	while len(received_data) < msg_size:
		received_data += client_socket.recv(4096)

	# Extract the frame data
	frame_data = received_data[:msg_size]
	received_data = received_data[msg_size:]

	# Deserialize the frame
	frame = pickle.loads(frame_data);
	ocr.set_exchange(frame)
	frame = ocr_from_frame(frame, ocr)

	# Display the frame
	cv2.imshow("from server", frame)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		print("Shutting down server...")
		break

# Release resources
cv2.destroyAllWindows()
client_socket.close()