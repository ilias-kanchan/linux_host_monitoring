from worker import Worker
import csv

filename = 'hosts.csv'

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for (host, user, password) in datareader:
        server = host
        user = user
        password = password

        cpu = Worker("top -b -n 1", server, user, password)
        cpu.info_collector()

        memory = Worker("free -g", server, user, password)
        memory.info_collector()

        disk = Worker("df -h", server, user, password)
        disk.info_collector()