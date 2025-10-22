import argparse
import fcntl
import os
import socket
import time

from datetime import datetime
from threading import Thread

LOG_FILE_PATH = "/home/rachel/cs644/http.log"


def run():
    print("running")
    try:
        sock = socket.socket(socket.AF_INET)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", 3000))
        # default backlog of 0:
        sock.listen()
        while True:
            conn, addr = sock.accept()
            # TODO: use _thread instead of Threading
            # https://docs.python.org/3/library/_thread.html#module-_thread
            t = Thread(target=handle_client, args=(conn,))
            t.start()
    except KeyboardInterrupt:
        # TODO: refactor to wait until all existing threads have terminated via t.join()
        # https://docs.python.org/3/library/threading.html#introduction
        print("Okay, bye!")
    finally:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()


def handle_client(conn):
    msg = bytearray()
    while True:
        data = conn.recv(1024)
        print(data)
        msg.extend(data)
        conn.send(b"ack\n")
        if not data:
            break
    fd = os.open(LOG_FILE_PATH, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
    fcntl.flock(fd, fcntl.LOCK_SH)
    # append line to log
    time_string = str(datetime.now())
    msg_string = msg.decode().replace("\n", " ")
    print_string = f"{time_string}: {msg_string}\n"
    print(print_string, end="")
    log_line = print_string.encode()
    os.write(fd, log_line)
    # close file
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)


def count():
    print("counting")
    line_count = 0
    try:
        # read log file and print count of lines
        fd = os.open(LOG_FILE_PATH, os.O_RDONLY)
        fcntl.flock(fd, fcntl.LOCK_SH)
        # empty file has empty bytestring
        # file with one line has no newlines but non-empty bytestring
        output = os.read(fd, 20).decode()
        # in a for loop, read file. keep counter of number of lines
        while output != "":
            line_count += len(output.splitlines())
            # don't overcount the second part of a line that has already been partially read
            output = os.read(fd, 20).decode().split("\n", 1)[-1]
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
    # rescue FileNotFoundError and return 0
    except FileNotFoundError:
        pass
    finally:
        print(f"Line count: {line_count}")


def main():
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--run", action="store_true")
    parser.add_argument("-c", "--count", action="store_true")
    args = parser.parse_args()

    if args.count:
        count()
    elif args.run:
        run()


if __name__ == "__main__":
    main()
