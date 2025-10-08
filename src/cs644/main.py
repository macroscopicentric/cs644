import argparse
import os
import time

from datetime import datetime

LOG_FILE_PATH = "/home/rachel/cs644/http.log"

def run():
    print("running")
    # TODO: fork four child processes
    # child processes run for a variable amount of time
    # return from loop below once all four children have exited
    while True:
        fd = os.open(LOG_FILE_PATH, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
        # append line to log
        time_string = str(datetime.now())
        print(time_string)
        log_line = f'{time_string}\n'.encode()
        os.write(fd, log_line)
        # close file
        os.close(fd)
        time.sleep(1)
    # print status code returns of four children

def count():
    print("counting")
    line_count = 0
    try:
        # read log file and print count of lines
        fd = os.open(LOG_FILE_PATH, os.O_RDONLY)
        # empty file has empty bytestring
        # file with one line has no newlines but non-empty bytestring
        output = os.read(fd, 20).decode()
        # in a for loop, read file. keep counter of number of lines
        while output != '':
            line_count += len(output.splitlines())
            # don't overcount the second part of a line that has already been partially read
            output = os.read(fd, 20).decode().split('\n', 1)[-1]
        os.close(fd)
    # rescue FileNotFoundError and return 0
    except FileNotFoundError:
        pass
    finally:
        print(f"Line count: {line_count}")

def main():
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run', action='store_true')
    parser.add_argument('-c', '--count', action='store_true')
    args = parser.parse_args()

    if args.count:
        count()
    elif args.run:
        run()

if __name__ == "__main__":
    main()
