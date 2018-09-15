import socket

def toggle_light(server_address, port, light_id_str, new_state):
    new_state_str = '1' if new_state else '0'
    cmd_str = light_id_str + ' ' + new_state_str
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (server_address, port) )
    sock.sendall(cmd_str.encode('utf-8') + b'\0')
    response = sock.recv(1024)
    sock.close()
    if (response != b'\1'):
        raise RuntimeError('Message was improperly formatted - not accepted by server')
