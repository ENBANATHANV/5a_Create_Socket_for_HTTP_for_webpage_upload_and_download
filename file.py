import socket
import base64

def send_request(host, port, request, headers=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        # Add additional headers if provided
        if headers:
            request = request + '\r\n' + '\r\n'.join([f'{key}: {value}' for key, value in headers.items()])
        s.sendall(request.encode())
        response = s.recv(4096).decode()
    return response

def upload_file(host, port, filename, headers=None):
    with open(filename, 'rb') as file:
        file_data = file.read()
        content_length = len(file_data)
        request = f"POST /upload HTTP/1.1\r\nHost: {host}\r\nContent-Length: {content_length}\r\n\r\n"
        request += file_data.decode()
        response = send_request(host, port, request, headers)
    return response

def download_file(host, port, filename, headers=None):
    request = f"GET /{filename} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    response = send_request(host, port, request, headers)
    file_content = response.split('\r\n\r\n', 1)[1]
    with open(filename, 'wb') as file:
        file.write(file_content.encode())

if __name__ == "__main__":
    host = 'example.com'
    port = 80

    # Example of adding an authentication header (if required)
    headers = {
        'Authorization': 'Bearer your_access_token_here',  # Add your token here if necessary
    }

    # Upload file
    upload_response = upload_file(host, port, 'example.txt', headers)
    print("Upload response:", upload_response)

    # Download file
    download_file(host, port, 'example.txt', headers)
    print("File downloaded successfully.")
