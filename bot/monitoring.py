import paramiko
import os
import logging
from pathlib import Path
from dotenv import load_dotenv


# Подключаем логирование
logging.basicConfig(
    filename='logfileMonitorBot.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


class MonitorBot:
    def __init__(self):
        # dotenv_path = Path('.env')
        # load_dotenv(dotenv_path=dotenv_path)

        self.host = os.getenv('RM_HOST')
        self.port = os.getenv('RM_PORT')
        self.username = os.getenv('RM_USER')
        self.password = os.getenv('RM_PASSWORD')

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.host, username=self.username, password=self.password, port=self.port)

    def get_output(self, channels):
        logging.debug(channels)
        stdin, stdout, stderr = channels
        data = (stdout.read() + stderr.read()).decode()
        #data = channels
        data = data.replace('\\n', '\n').replace('\\t', '\t')
        logging.debug(data)
        return data

    def get_release(self):
        res = self.client.exec_command('lsb_release -r')
        logging.debug(res)
        return self.get_output(res)

    def get_uname(self):
        res = self.client.exec_command('uname')
        logging.debug(res)
        return self.get_output(res)

    def get_uptime(self):
        res = self.client.exec_command('uptime')
        logging.debug(res)
        return self.get_output(res)

    def get_df(self):
        res = self.client.exec_command('df -h')
        logging.debug(res)
        return self.get_output(res)

    def get_free(self):
        res = self.client.exec_command('free -h')
        logging.debug(res)
        return self.get_output(res)

    def get_mpstat(self):
        res = self.client.exec_command('mpstat')
        logging.debug(res)
        return self.get_output(res)

    def get_w(self):
        res = self.client.exec_command('w')
        logging.debug(res)
        return self.get_output(res)

    def get_auths(self):
        res = self.client.exec_command('cat /var/log/auth.log | grep "New session" | tail')
        logging.debug(res)
        return self.get_output(res)

    def get_critical(self):
        res = self.client.exec_command('journalctl -p crit | tail -n 5')
        logging.debug(res)
        return self.get_output(res)

    def get_ps(self):
        res = self.client.exec_command('ps')
        logging.debug(res)
        return self.get_output(res)

    def get_ss(self):
        res = self.client.exec_command('ss -t')
        logging.debug(res)
        return self.get_output(res)

    def get_apt_list(self, packet=None):
        cmd = "apt list --installed | grep -v automatic | grep -v upgradable | cut -d '/' -f1"
        if packet:
            logging.debug(packet)
            cmd = f'apt list --installed | grep {packet}'
        
        logging.debug(cmd)
        res = self.client.exec_command(cmd)
        logging.debug(res)
        return self.get_output(res) 

    def get_services(self):
        res = self.client.exec_command('service --status-all')
        logging.debug(res)
        return self.get_output(res)

    def get_repl_logs(self):
        res = self.client.exec_command('tail /var/log/postgresql/postgres*.log -n 10')
        logging.debug(res)
        return self.get_output(res)
