import cv2
import socket
import pickle
import struct

video = cv2.VideoCapture(0)
desired_width = 1920
desired_height = 1080
video.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

# Creates the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("0.0.0.0", 8001))

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(("0.0.0.0", 8001))
# server_socket.listen(10)

# client_socket, address = server_socket.accept()
print(f"Connection to server has been established.")

while True:
	ret, frame = video.read()
	serialized_frame = pickle.dumps(frame)
	message_size = struct.pack("L", len(serialized_frame))
	client_socket.sendall(message_size + serialized_frame)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

video.release()
cv2.destroyAllWindows()

client_socket.close()
server_socket.close()