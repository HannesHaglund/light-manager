import os
import time
import socket
import threading

def _handle_client_request(client, dry_run, toggle_attempts_to_make):
    '''
    Receive messages that adheres to the following form:
    b'<system id> <device id> <state>\0'
    Encoding must be utf-8.
    The two first arguments are castable to ints, and the last is 0 or 1.
    The server responds with '1' if succesful or '0' if not, encoded as utf-8.
    '''
    def toggle_outlet(system_id, device_id, new_state):
        for i in range(toggle_attempts_to_make):
            os.system('send ' \
                      + system_id + ' ' \
                      + device_id + ' ' \
                      + new_state)

    def receive_msg():
        chunks = b''
        while True:
            chunk = client.recv(1024)
            if chunk == b'':
                return []
            chunks += chunk
            if b'\0' in chunk:
                break
        msg = chunks.split(b'\0')[0].decode('utf-8')
        args = msg.split(' ')
        return args

    def verify_args(args):
        if len(args) != 3:
            return False
        for arg in args:
            for char in arg:
                if char not in '0123456789':
                    return False
        if args[2] != '0' and args[2] != '1':
            return False
        return True

    def send_response(return_status):
        msg = b'\1' if return_status else b'\0'
        sent = client.send(msg)
        if sent <= 0:
            raise RuntimeError('Socket broken')

    args = receive_msg()
    print('Incoming msg:', args)
    if verify_args(args):
        if not dry_run:
            toggle_outlet(args[0], args[1], args[2])
            print('Outlet was succesfully toggled (args=', args, ')')
        else:
            print('Outlet was not toggled due to dry run (args=', args, ')')
        send_response(True)
    else:
        print('Error:', args, 'are not valid')
        send_response(False)
    client.close()

def loop(hostname, port, \
         dry_run = False, \
         queue_limit = 5, \
         socket_timeout = 60, \
         toggle_attempts_to_make = 2):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind( (hostname, port) )
    sock.listen(queue_limit)

    while True:
        print(sock.getsockname()[0], 'listening on port', port)
        client, address = sock.accept()
        client.settimeout(socket_timeout)
        print('Incoming client, address =', address)
        thread = threading.Thread(target=_handle_client_request, \
                         args=(client, dry_run, toggle_attempts_to_make))
        thread.start()
        thread.join()

if __name__ == '__main__':
    loop('', 5347, True)
