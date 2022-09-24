# This is a simple script to terminate processes blocking ports on your computer
from time import sleep

from psutil import process_iter
from signal import SIGTERM

debug = False


def print_logo():
    print("""
    +-+-+-+-+ +-+-+-+-+-+-+-+
    |P|o|r|t| |C|l|e|a|n|e|r|
    +-+-+-+-+ +-+-+-+-+-+-+-+
    by Tarek St.
    """)


# searches the process
def find_process(search_port):
    # iterating through all processes
    for process in process_iter(['pid', 'name', 'connections']):
        if debug:
            print("---------------------")
            print(process.name() + " - PID: " + str(process.ppid()))
        # iterating through all connections of the process
        for connection in process.connections():
            port = connection.laddr.port
            if debug:
                print("Port -> " + str(port))
            if port == search_port:
                return process
    return None


def main():
    print_logo()
    # port input
    port = int(input("Please enter the port to be terminated: "))
    process = find_process(port)
    if process is None:
        # process found
        print("No process found using port " + str(port))
    else:
        # found process
        print("Found process " + process.name() + " using port " + str(port))
        print("Terminating " + process.name() + " (" + str(process.pid) + ") ...")
        # sending terminate signal to the process
        # TODO: add kill signal support to terminate all child processes (aggressive mode)
        process.send_signal(SIGTERM)
        sleep(1)
        try:
            if process.status() == "running":
                print("Could not terminate process " + process.name() + " (" + str(process.pid) + ")")
        except:
            print("Terminated process! Port " + str(port) + " should be clear")


if __name__ == '__main__':
    main()
