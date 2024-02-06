import os
import socket

IP = input("Enter server address:")
PORT = 8000
SIZE = 1024
FORMAT = "utf"
UPLOAD_FOLDER = "upload_folder"
DOWNLOAD_FOLDER = "download_folder"

""" Starting a tcp socket """
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
print("Connection Succesfull")

def download():
    """ Receiving files """
    while True:
        msg = client.recv(SIZE).decode(FORMAT)
        cmd, data = msg.split(":")

        if cmd == "FILENAME":
            """ Recv the file name """
            print(f"[CLIENT] Downloading the filename: {data}.")

            file_path = os.path.join(DOWNLOAD_FOLDER, data)
            file = open(file_path, "w")
            client.send("Filename downloaded.".encode(FORMAT))

        elif cmd == "DATA":
            """ Recv data from client """
            print(f"[CLIENT] Downloading the file data.")
            file.write(data)
            client.send("File data Downloaded".encode(FORMAT))

        elif cmd == "FINISH":
            file.close()
            print(f"[CLIENT] {data}.\n")
            client.send("The data is Downloaded.".encode(FORMAT))

        elif cmd == "CLOSE":
            print(f"[CLIENT] {data}")
            break

def upload():
    """ Sending files """
    files = sorted(os.listdir(UPLOAD_FOLDER))

    for file_name in files:
        """ Send the file name """
        msg = f"FILENAME:{file_name}"
        print(f"[CLIENT] Uploading file name: {file_name}")
        client.send(msg.encode(FORMAT))

        """ Recv the reply from the server """
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

        """ Send the data """
        file = open(os.path.join(UPLOAD_FOLDER, file_name), "r")
        file_data = file.read()

        msg = f"DATA:{file_data}"
        client.send(msg.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

        """ Sending the close command """
        msg = f"FINISH:Complete data Uploaded"
        client.send(msg.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

    """ Closing the connection from the server """
    msg = f"CLOSE:File transfer is completed"
    client.send(msg.encode(FORMAT))

while True:
    choice = input("1) Upload \n2) Download \n3) Exit\n")
    if(choice == "1"):
        client.send("upload".encode(FORMAT))
        upload()
    elif(choice == "2"):
        client.send("download".encode(FORMAT))
        download()
    else:
        client.send("exit".encode(FORMAT))
        client.close()
        exit()