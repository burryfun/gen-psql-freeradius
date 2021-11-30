#!/usr/bin/python3
import psycopg2
import random
import ctypes
import string
import subprocess
import json
from functools import partial

# IMPORT GENERATOR USERNAME
from gen_name import GenUser

# IMPORT C FUNC FOR IP ADDRESS CALCULATION
ipaddr_calc = ctypes.CDLL('./lib/ipaddrcalc')
ipaddr_calc.maxIP.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
ipaddr_calc.maxIP.restype = ctypes.c_char_p

DB_NAME = 'radius'
DB_USER = 'radius'
DB_PASS = 'radius'
DB_HOST = 'localhost'

DB_SQLFILEPATH = 'sub_db.sql'
JSON_FILEPATH = 'subscribers.json'

COUNT_SUBS = 10
START_IP = '192.168.1.100'
PASS_LEN = 5


def random_mac ():
    c = partial(random.randint, 0 ,255)
    return '%02x:%02x:%02x:%02x:%02x:%02x' % (c(), c(), c(), c(), c(), c())

def random_pass(length=PASS_LEN):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def save_psqldb(host, database_name, user, password, dest_file, port=5432):
    """
    Backup postgres db to a file.
    """
    try:
        process = subprocess.Popen(
            ['pg_dump',
                '--dbname=postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database_name),
                '-f', dest_file,],
            stdout=subprocess.PIPE
        )
        output = process.communicate()[0]
        if int(process.returncode) != 0:
            print('Command failed. Return code : {}'.format(process.returncode))
            exit(1)
        return output
    except Exception as e:
        print(e)
        exit(1)

class Subscriber:
    def __init__(self):
        Subscriber._counter += 1

        if Subscriber._ip_counter == START_IP:
            b_string = ctypes.c_char_p(ipaddr_calc.maxIP(START_IP.encode('utf-8'), 2)).value
            Subscriber._ip_counter = b_string.decode('utf-8')
        else:
            b_string = ctypes.c_char_p(ipaddr_calc.maxIP(Subscriber._ip_counter.encode('utf-8'), 2)).value
            Subscriber._ip_counter = b_string.decode('utf-8')

        self.id = Subscriber._counter
        self.ip = Subscriber._ip_counter
        self.username = GenUser().new() + '_' + str(self.id)
        self.password = random_pass()
        self.mac = random_mac()

    _counter = 0
    _ip_counter = START_IP

def main():

    conn = psycopg2.connect(dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST)

    with conn:
        with conn.cursor() as cur:
            
            # IMPORT FREERADIUS SCHEMA
            cur.execute(f"drop owned by {DB_USER};")
            cur.execute(open("schema.sql", "r").read())

            # CREATE TABLE WITH SUBSCRIBERS
            cur.execute("create table subscribers( \
                            id			    serial PRIMARY KEY,    \
                            ip              text NOT NULL, \
                            username		text NOT NULL, \
                            password		text NOT NULL, \
                            mac    		    text NOT NULL  \
                        );")

            subs = []
            # GENERATE SUBSCRIBERS AND FILL DB
            for _ in range(COUNT_SUBS):
                sub = Subscriber()
                cur.execute("insert into radcheck(username, attribute, op, value) \
                                         values(%s, 'Cleartext-Password', ':=', %s);",
                                         (sub.username, sub.password))
                cur.execute("insert into radreply(username, attribute, value) \
                                         values(%s, 'Framed-IP-Address', %s);", 
                                         (sub.username, sub.ip))
                cur.execute("insert into subscribers(ip, username, password, mac) \
                                         values(%s, %s, %s, %s);",
                                         (sub.ip, sub.username, sub.password, sub.mac))
                subs.append(sub.__dict__)

            # SAVE SUBS TO JSON
            with open(JSON_FILEPATH, 'w') as json_file:
                json.dump(subs, json_file)

    return

if __name__ == '__main__':
    main()