from fabric import Connection
import logging
import paramiko
logging.basicConfig(filename='Log.txt',level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
host = '192.168.0.102'
user_name = 'kali'
user_password = 'kali'

def get_release():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('lsb_release -a')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'


def get_uname():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('uname -a')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_uptime():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('uptime')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_df():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('df -h')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_free():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('free -h')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_mpstat():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('top -b -n 1')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_w():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('w')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_auths():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('last -n 10')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_critical():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('cat /var/log/syslog | grep -i "critical" | tail -n 5')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_ps():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('ps aux')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_ss():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('netstat -tuln')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_apt_list():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('dpkg --get-selections')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_apt_list_arg(packet):
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run(f'apt show {packet}')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'
def get_services():
    try:
        with Connection(host=host, user=user_name, connect_kwargs={'password': user_password}) as conn:
            result = conn.run('service --status-all')
            result = result.stdout.strip()
        return result
    except Exception as ex:
        
        return f'Ошибка:{ex}'


def get_repl_logs():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user_name, password=user_password, port=22)
        stdin, stdout, stderr = client.exec_command('docker logs bot_image_repl --tail 20')
        data = stdout.read() + stderr.read()
        client.close()
        return data.decode('utf8')
    except Exception as ex:
        
        return f'Ошибка:{ex}'
