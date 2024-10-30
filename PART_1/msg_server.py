import os
import sys
import socket
import threading
import datetime
import pytz
import json

ACCEPTED_METHOD = ('GET', 'POST')

CONTENT_TYPE = {
    'json' : 'application/json',
    'html' : 'text/html',
    'txt' : 'text/plain',
    'png' : 'image/png'
}

# global variable to hold message boards
BOARD_LIST = {'list1.json', 'list2.json', 'list3.json', 'list4.json', 'list5.json', 'html_test.html', 'image_test.html', 'my_image.png'}

HOST = ''
PORT = int(sys.argv[1])
FLAG = '-m'

if len(sys.argv) == 3 and sys.argv[2] == FLAG:
    print('Server run in multi-threaded mode')
elif len(sys.argv) == 2 and FLAG not in sys.argv:
    print('Server run in single-threaded mode')
else:
    print('Run progrom by this command: python3 msg_server.py <port number> (<-m> for multi-threaded).')


# Define a function to get the last modified time of a file
def get_last_modified_time(file_path):
   lastUpdatedPattern = "%a, %d %b %Y %H:%M:%S %Z"
   modifiedTimestamp = os.path.getmtime(file_path)
   # hardcoding Winnipeg for simplicity
   modifiedTime = datetime.datetime.fromtimestamp(modifiedTimestamp, tz=pytz.timezone("America/Winnipeg"))
   return modifiedTime.strftime(lastUpdatedPattern)

def update_board_html(board_name):
    # Load existing board.html content
    with open('board.html', 'r') as file:
        lines = file.readlines()

    # Find the <ul> element to insert the new link
    for i, line in enumerate(lines):
        if '<ul>' in line:
            insert_index = i + 1
            break
    else:
        insert_index = -1

    # Generate the new link HTML
    new_link = f'<li><a href="{board_name}">{board_name}</a></li>\n'

    # Insert the new link into the list
    if insert_index != -1:
        lines.insert(insert_index, new_link)
    else:
        # If no <ul> found, add it at the end 
        lines.append('<ul>\n')
        lines.append(new_link)
        lines.append('</ul>\n')

    # Save the updated content back to board.html
    with open('board.html', 'w') as file:
        file.writelines(lines)


def handle_connection(client_socket):
    try:
        with client_socket:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                return
            
            request_lines = data.split('\r\n')
            request_line = request_lines[0]
            request_method, request_path, _ = request_line.split()
            print('The request path is:', request_path)

            # handle the GET request
            if request_method == 'GET':    
                # a request to '/' to return html page that lists all the boards
                if request_path == '/':
                    last_modified = get_last_modified_time('board.html')
                    with open('board.html', 'rb') as file:
                        body = file.read()
                        client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                        client_socket.sendall(body)

                # check if the item requested is in the list of board
                elif request_path.strip('/').split('/')[0] in BOARD_LIST:
                    parts = request_path.strip('/').split('/')
                    board_name = parts[0]

                    path_file = f'./{board_name}'
                    basename = os.path.basename(board_name)
                    extend = basename.split('.')[1]
                    last_modified = get_last_modified_time(path_file)
                    # GET request the content type json
                    if extend == 'json':
                        if os.path.exists(path_file):
                            with open(path_file, 'r') as file:
                                body = json.load(file)
                                # a request to /<board>/ to return all message from that board
                                if len(parts) == 1:
                                    client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(json.dumps(body).encode())}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                                    client_socket.sendall(json.dumps(body).encode())

                                # a request to /<board>/<message_index> to return the message at the given index 
                                elif len(parts) == 2:
                                    message_index = parts[1]
                                    value_entry = body.get(message_index)
                                    if value_entry:
                                        client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(json.dumps({message_index : value_entry}).encode())}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                                        client_socket.sendall(json.dumps({message_index : value_entry}).encode())
                                    else:
                                        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nMessage not found.")
                        else:
                            client_socket.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nBoard not found.")
                    # GET request the content type html
                    elif extend == 'html':
                        if os.path.exists(path_file):
                            with open(path_file, 'rb') as file:
                                body = file.read()
                                # a request to /<board>/ to return all message from that board
                                if len(parts) == 1:
                                    client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                                    client_socket.sendall(body)
                                elif len(parts) == 2:
                                    message_index = parts[1]
                                    if message_index == '1':
                                        body = b'{"1" : "hello"}'
                                        client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                                        client_socket.sendall(body)
                                    elif message_index == '2':
                                        body = b'{"2" : "how are you"}'
                                        client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                                        client_socket.sendall(body)
                                    elif message_index == '3':
                                        body = b'{"3" : "ok my friends"}'
                                        client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                                        client_socket.sendall(body)
                                    else:
                                        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nMessage not found.")
                    elif extend == 'png':
                        if os.path.exists(path_file):
                            with open(path_file, 'rb') as file:
                                body = file.read()
                                client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: image/png\r\nContent-Length: {len(body)}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                                client_socket.sendall(body)


                else:
                    client_socket.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFile not found.")
            # handle the POST request
            elif request_method == 'POST':
                parts = request_path.strip('/').split('/')
                _, content_type = request_lines[4].split(': ')
                print("The content type is:", content_type)

                # the content type is json 
                if content_type == CONTENT_TYPE['json']:
                    
                    json_message = request_lines[7]
                    json_part = json.loads(json_message)

                    # a request to /<board>/ which add provided message to given board
                    if len(parts) == 1:
                        board_name = parts[0]

                        # check if the board is not existed in the list
                        if board_name not in BOARD_LIST:
                            BOARD_LIST.add(board_name)
                            update_board_html(board_name)

                            # create new json file with new board name
                            path_file = f'./{board_name}'

                            # check if name not exist in the file system
                            if not os.path.exists(path_file):
                                # open file in write mode, if file not exist, it will be created
                                with open(path_file, 'w') as bf:
                                    # write an empty json object
                                    json.dump({}, bf)
                        
                            # open the file in read-write mode
                            with open(path_file, 'r+') as bf:
                                # read the current content of the file
                                try:
                                    board_data = json.load(bf)
                                except json.JSONDecodeError:
                                    # if the file is empty or contains invalid JSON, initialize an empty dictionary
                                    board_data = {}
                                
                                # update the board data with the new POST content
                                board_data.update(json_part)
                                
                                # seek to the beginning of the file and truncate it
                                bf.seek(0)
                                bf.truncate()

                                # write the updated content to the file
                                json.dump(board_data, bf)
                            last_modified = get_last_modified_time(path_file)
                            client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(json.dumps(board_data).encode())}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                            client_socket.sendall(json.dumps(board_data).encode())
                        
                        # the board is existed, add new json message to that board
                        else:
                            path_file = f'./{board_name}'

                            with open(path_file, 'r+') as bf:
                                # read the current content of the file
                                try:
                                    board_data = json.load(bf)
                                except json.JSONDecodeError:
                                    # if the file is empty or contains invalid JSON, initialize an empty dictionary
                                    board_data = {} 
                            
                                # update the board data with the new POST content
                                board_data.update(json_part)
                                    
                                # seek to the beginning of the file and truncate it
                                bf.seek(0)
                                bf.truncate()

                                # write the updated content to the file
                                json.dump(board_data, bf)
                            last_modified = get_last_modified_time(path_file)
                            client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(json.dumps(board_data).encode())}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                            client_socket.sendall(json.dumps(board_data).encode())
                    else:
                        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nPath not found.")
                elif content_type == CONTENT_TYPE['html']:
                    html_message = request_lines[7]

                    if len(parts) == 1:
                        board_name = parts[0]

                        if board_name not in BOARD_LIST:
                            BOARD_LIST.add(board_name)
                            update_board_html(board_name)

                            # create new html file with new board name
                            path_file = f'./{board_name}'
                            print('The path file is:', path_file)
                            # check if name not exist in the file system
                            if not os.path.exists(path_file):
                                # open file in write mode, if file not exist, it will be created
                                with open(path_file, 'wb') as file:
                                    body = html_message.encode()
                                    file.write(body)
                                    last_modified = get_last_modified_time(path_file)
                                    client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                                    client_socket.sendall(body)

                        else:
                            path_file = f'./{board_name}'
                            with open(path_file, 'rb') as file:
                                body = file.read()
                                body += html_message.encode()
                                last_modified = get_last_modified_time(path_file)
                                client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\nLast-Modified: {last_modified} \r\nServer: Namikaze Minato\r\n\r\n".encode())
                                client_socket.sendall(body)
                    else:
                        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nPath not found.")
            else:
                client_socket.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nRequest method not found.")

    except Exception as e:
        print(f"Error handling connection: {e}")
        client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nServer error.")

    finally:
        client_socket.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        print(f'Server is listening on host {HOST} and port {PORT}')

        while True:
            try:
                conn, addr = server_socket.accept()
                print(f'Server connected to {addr}')
                # switch between single-threaded and multi-threaded
                if len(sys.argv) == 3 and sys.argv[2] == FLAG: #multi-threaded
                    threading.Thread(target=handle_connection, args=(conn,)).start()
                else: # single-threaded
                    handle_connection(conn,)
            except KeyboardInterrupt:
                print("\nServer is shutting down.")
                sys.exit()
            except Exception as e:
                print(f"Server error: {e}")

if __name__ == "__main__":
    start_server()
