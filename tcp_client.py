import socket

target_host = "10.197.147.32"   # removed trailing space
target_port = 53

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(5)

try:
    client.connect((target_host, target_port))
    print(f"[+] Connected to {target_host}:{target_port}")

    # ⚠️ Port 53 expects DNS packets, NOT HTTP.
    # Sending HTTP will likely get no meaningful reply.
    client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\nConnection: close\r\n\r\n")

    chunks = []
    while True:
        data = client.recv(4096)
        if not data:
            break
        chunks.append(data)

    response = b"".join(chunks)
    print("[+] Response:")
    print(response.decode(errors="ignore"))

except socket.timeout:
    print("[-] Connection timed out")
except ConnectionRefusedError:
    print("[-] Connection refused (port closed)")
except Exception as e:
    print(f"[-] Error: {e}")
finally:
    client.close()
    print("[+] Connection closed")

#     import socket

# target_host = "10.197.147.32 "   # ⚠️ trailing space is a bug
# target_port = 53                 # Port 53 = DNS
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
# client.connect((target_host, target_port))                   # connect
# client.send(b"GET / HTTP/1.1\r\nHost: google.com \r\n\r\n")  # send raw HTTP
# response = client.recv(4096)                                 # read up to 4KB
# print(response.decode())
# client.close()