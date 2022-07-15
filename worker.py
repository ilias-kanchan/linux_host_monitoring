import paramiko
import datetime
import os


class Worker:

    def __init__(self, command, server, user, password):
        self.command = command
        self.server = server
        self.user = user
        self.password = password

    def info_collector(self):
        server_ip = self.server
        username = self.user
        password = self.password

        x = datetime.datetime.now()
        today_date = x.strftime("%Y_%m_%d")
        try:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server_ip, username=username, password=password)
            stdin, stdout, stderr = client.exec_command("hostname")
        except:
            print(f"Wrong username and password for host {server_ip}")
            pass
        else:
            # print(stdout.read().decode())
            hostname = stdout.read().decode().strip('\n')
            hostname_date = hostname + "_" + today_date
            # print(hostname_date.strip('\n'))
            log_path = './log'
            isexist = os.path.exists(log_path)
            if not isexist:
                os.makedirs(log_path)
            # print(hostname_date)
            stdin, stdout, stderr = client.exec_command(self.command)
            command_info = stdout.read().decode()
            # print(cpu_utilization)
            with open(f"{log_path}/{hostname_date}.txt", "a+") as f:
                x = datetime.datetime.now()
                today_date_time = x.strftime("%Y_%m_%d_%H_%M_%S_yyyy_mm_dd_hr_min_sec")
                f.write(f"=======================Today is {today_date_time}====================running command===== {self.command}\n{command_info}")

            stdin.close()
            client.close()
