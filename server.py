import os
import socket

IP = input("Enter your address:")
PORT = 8000
SIZE = 1024
FORMAT = "utf"
UPLOAD_FOLDER = "upload_folder"
DOWNLOAD_FOLDER = "download_folder"

print("[STARTING] Server is starting.\n")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
print("[LISTENING] Server is waiting for clients.")

def download(conn):
    """ Receiving files """
    while True:
        msg = conn.recv(SIZE).decode(FORMAT)
        cmd, data = msg.split(":")

        if cmd == "FILENAME":
            """ Recv the file name """
            print(f"[CLIENT] Downloaded the filename: {data}.")

            file_path = os.path.join(DOWNLOAD_FOLDER, data)
            file = open(file_path, "w")
            conn.send("Filename uploaded".encode(FORMAT))

        elif cmd == "DATA":
            """ Recv data from client """
            print(f"[CLIENT] downloading the file data.")
            file.write(data)
            conn.send("File data uploaded".encode(FORMAT))

        elif cmd == "FINISH":
            file.close()
            print(f"[CLIENT] {data}.\n")
            conn.send("The data is saved.".encode(FORMAT))

        elif cmd == "CLOSE":
            print(f"[CLIENT] {data}")
            break

def upload(conn):
    """ Sending files """
    files = sorted(os.listdir(UPLOAD_FOLDER))

    for file_name in files:
        """ Send the file name """
        msg = f"FILENAME:{file_name}"
        print(f"[CLIENT] Uploading the filename: {file_name}")
        conn.send(msg.encode(FORMAT))

        """ Recv the reply from the server """
        msg = conn.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

        """ Send the data """
        file = open(os.path.join(UPLOAD_FOLDER, file_name), "r")
        file_data = file.read()

        msg = f"DATA:{file_data}"
        conn.send(msg.encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

        """ Sending the close command """
        msg = f"FINISH:Complete data send"
        conn.send(msg.encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

    """ Closing the connection from the server """
    msg = f"CLOSE:Uploaded the data"
    conn.send(msg.encode(FORMAT))

def handleConnection(conn):
    while True:
        choice = conn.recv(SIZE).decode(FORMAT)
        if(choice == "upload"):
            download(conn)
        elif(choice == "download"):
            upload(conn)
        elif(choice == "exit"):
            break

while True:
    conn, addr = server.accept()
    print(f"[NEW CONNECTION] {addr} connected.\n")
    handleConnection(conn)