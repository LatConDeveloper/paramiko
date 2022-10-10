import time
import sys

import paramiko
from scp import SCPClient
# python main.py 68.183.27.136 latconsulting.tech erick gerard root LatDev852/ root LatDev852
if __name__ == '__main__':
    # Read in the file

    try:
        remote_server_1 = sys.argv[1]
        remote_server_2 = sys.argv[2]

        text_find = sys.argv[3]
        text_replace = sys.argv[4]

        remote_server_1_username = sys.argv[5]
        remote_server_1_password = sys.argv[6]

        remote_server_2_username = sys.argv[7]
        remote_server_2_password = sys.argv[8]
    except Exception:
        print("Wrong Parameters")
        exit()

    # setup client A
    client_1 = paramiko.SSHClient()
    client_1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print("Server A: connecting...")
        client_1.connect(remote_server_1, username=remote_server_1_username, password=remote_server_1_password)
        print("Server A: connected")
    except paramiko.ssh_exception.AuthenticationException as e:
        print("Invalid Credentials of Server A")
        exit()

    # setup client B
    client_2 = paramiko.SSHClient()
    client_2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print("Server B: connecting...")
        client_2.connect(remote_server_2, username=remote_server_2_username, password="remote")
        print("Server B: connected")
    except paramiko.ssh_exception.AuthenticationException as e:
        print("Invalid Credentials of Server B")
        exit()

    # Get /root/test.txt
    try:
        ftp_client_1 = client_1.open_sftp()
        ftp_client_1.get('/root/config.txt', 'config.txt')
        ftp_client_1.close()
    except FileNotFoundError as e:
        print("Invalid File")
    ###

    # replace txt
    print("updating file")
    f = open('config.txt', 'r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace(text_find, text_replace)
    f = open('config.txt', 'w')
    f.write(newdata)
    f.close()
    print("done")
    ####

    # Upload
    try:
        print("copying")
        ftp_client_2 = client_2.open_sftp()
        ftp_client_2.put('config.txt', '/home/test/config.txt')
        ftp_client_2.close()
    except FileNotFoundError as e:
        print("Invalid File")
        exit()

    print("Success!!")
