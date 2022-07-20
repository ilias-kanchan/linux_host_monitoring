import paramiko
import smtplib, ssl
import datetime
import csv
import os

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "sender@gmail.com"  # Enter your address
receiver_email = "receiver@gmail.com"  # Enter receiver address
mail_password = "pass123"


class Mailer:

    def __init__(self, command, server, user, password):
        self.command = command
        self.server = server
        self.user = user
        self.password = password

    def cpu_mailer(self):
        server_ip = self.server
        username = self.user
        password = self.password
        try:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server_ip, username=username, password=password)
            stdin, stdout, stderr = client.exec_command(self.command)
        except:
            print(f"Wrong username and password for host {server_ip}")
            pass
        else:
            cpu_utilization = float(stdout.read().decode())
            # print(cpu_utilization)
            if cpu_utilization >= 80:
                message = f"Subject: CPU utilization is high on server {server_ip}\n\nCPU utilization is {cpu_utilization}%"
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, mail_password)
                    server.sendmail(sender_email, receiver_email, message)
            else:
                print("cpu utilization is normal")
            stdin.close()
            client.close()

    def memory_mailer(self):
        server_ip = self.server
        username = self.user
        password = self.password
        try:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server_ip, username=username, password=password)
            stdin, stdout, stderr = client.exec_command(self.command)
        except:
            print(f"Wrong username and password for host {server_ip}")
            pass
        else:
            memory_utilization = float(stdout.read().decode())
            # print(memory_utilization)
            if memory_utilization >= 80:
                message = f"Subject: Memory utilization is high on server {server_ip}\n\nMemory utilization is {memory_utilization}%"
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, mail_password)
                    server.sendmail(sender_email, receiver_email, message)
            else:
                print("memory utilization is normal")
            stdin.close()
            client.close()

    def high_disk_utilization(self):
        server_ip = self.server
        username = self.user
        password = self.password
        # print(self.command)
        try:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server_ip, username=username, password=password)
            stdin, stdout, stderr = client.exec_command(self.command)
        except:
            print(f"Wrong username and password for host {server_ip}")
            pass
        else:
            disk_utilization = stdout.read().decode()

            disk_utilization = disk_utilization.replace("%", ",")

            with open("disk_utilization.csv", "w") as f:
                f.write(disk_utilization)

            with open("disk_utilization.csv", 'r') as csvfile:
                datareader = csv.reader(csvfile)
                for (utilization, mountpoint) in datareader:
                    if int(utilization) > 80:
                        # print(f"Host: {server_ip} Mountpoint {mountpoint} Utilization {utilization}")
                        with open("high_disk_utilization.txt", "a+") as f:
                            x = datetime.datetime.now()
                            today_date_time = x.strftime("%Y_%m_%d_%H_%M_%S_yyyy_mm_dd_hr_min_sec")
                            f.write(f"Date time: {today_date_time} Host: {server_ip} Mountpoint {mountpoint} Utilization {utilization}%\n")

            stdin.close()
            client.close()

    def high_disk_mailer(self):

        try:
            with open("high_disk_utilization.txt") as f:
                content = f.read()
        except FileNotFoundError:
            print("file not exist")
        else:
            message = f"Subject: Disk utilization is high\n\nDisk utilization is\n\n {content}"
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, mail_password)
                server.sendmail(sender_email, receiver_email, message)

        os.remove("high_disk_utilization.txt")

