from worker import Worker
from mailer import Mailer
import csv
import datetime

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

        cpu_utilization = Mailer("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'", server, user, password)
        cpu_utilization.cpu_mailer()

        memory_utilization = Mailer("free -m | grep 'Mem' | awk '{Mem=($2-($4+$7))/$2 * 100} END {print Mem}'", server, user, password)
        memory_utilization.memory_mailer()

        try:
            with open("today.txt") as f:
                today = f.read()
        except FileNotFoundError:
            with open("today.txt", "w") as f:
                x = datetime.datetime.now()
                today_date = x.strftime("%Y%m%d")
                f.write(today_date)
        else:
            x = datetime.datetime.now()
            today_date = x.strftime("%Y%m%d")
            if today_date == today:
                print("date matched")
            else:
                disk_utilization = Mailer("df -h | awk '{print $5 $6}' | grep -v 'Use'", server, user, password)
                disk_utilization.high_disk_utilization()

with open("today.txt") as f:
    today = f.read()

x = datetime.datetime.now()
today_date = x.strftime("%Y%m%d")

if today_date == today:
    print("date matched")
else:
    disk_utilization_mailer = Mailer("df -h | awk '{print $5 $6}' | grep -v 'Use'", server, user, password)
    disk_utilization_mailer.high_disk_mailer()
    with open("today.txt", "w") as f:
        x = datetime.datetime.now()
        today_date = x.strftime("%Y%m%d")
        f.write(today_date)

    with open("high_disk_utilization.txt", "w") as f:
        f.write("")
