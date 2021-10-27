# -*- coding: utf-8 -*-

# realtime data logger script by Akram Ali
# Updated on 10/05/2021

from datetime import datetime
from influxdb import InfluxDBClient
import time
from pathlib import Path
import subprocess

# get hostname of Pi to identify which one it is
hostname = subprocess.check_output('hostname', shell=True).strip()

now = datetime.now()   # get current date/time
logging_start_time = now.strftime('%Y-%m-%d_%H%M%S')    # format datetime to use in filename
temp_data_dir = '/var/tmp/temp_heatflux'
data_dir = '/home/pi/heatflux/data'
server = 'server-url'
influx_port = 8086
user = 'user'
passwd = 'password'
db = 'database'

time.sleep(10) # sleep 10 seconds to let data come in first


# function to find, parse, log and upload data files
def logdata(_dt):

    # get data from temp file
    try:
        file = open('%s/t.csv' % (temp_data_dir),'r')        
        dataline = file.readline()
        file.close()
    except:
        print ("failed to open temp file")
        pass

    # parse data
    data = []
    try:
        for p in dataline.strip().split(","): #strip() removes trailing \n
            data.append(p)
    except:
        pass

    # save data to file
    filename = '%s/%s_%s_%s.csv' % (data_dir, hostname, 'heatflux', logging_start_time)
    my_file = Path(filename)
    if my_file.is_file():   # if file already exists, i.e., logging started
        try:
            file = open(filename,'a')   # open file in append mode
            file.write(str(_dt) + ',')   # write formatted datetime
            file.write(dataline)
            # file.write('\n')
            file.close()
        except:
            print ('Error: Failed to open file %s' % filename)
            pass
    
    # file does not exist, write headers to it, followed by data. This should happen first time when creating file only
    else:   
        try:
            file = open(filename,'w')   # open file in write mode
            file.write('Date/Time')
            for n in range(1,9):
                file.write(',')
                if n % 2 == 0:
                    file.write('Temperature (C) (Ch %d)' % int(n/2))
                else:
                    file.write('Heat Flux (W/m2) (Ch %d)' % round(n-n/2))
            file.write('\n')
            file.close()
        except:
            pass


    # upload data
    json_body = [   # first create JSON body
        {
            "measurement": "heatflux",
            "tags": {
                "pi": hostname,
                "channel": 1
            },
            "fields": {
                "value": float(data[0])
            }
        },
        {
            "measurement": "temperature",
            "tags": {
                "pi": hostname,
                "channel": 1
            },
            "fields": {
                "value": float(data[1])
            }
        },
                {
            "measurement": "heatflux",
            "tags": {
                "pi": hostname,
                "channel": 2
            },
            "fields": {
                "value": float(data[2])
            }
        },
        {
            "measurement": "temperature",
            "tags": {
                "pi": hostname,
                "channel": 2
            },
            "fields": {
                "value": float(data[3])
            }
        },
                {
            "measurement": "heatflux",
            "tags": {
                "pi": hostname,
                "channel": 3
            },
            "fields": {
                "value": float(data[4])
            }
        },
        {
            "measurement": "temperature",
            "tags": {
                "pi": hostname,
                "channel": 3
            },
            "fields": {
                "value": float(data[5])
            }
        },
                {
            "measurement": "heatflux",
            "tags": {
                "pi": hostname,
                "channel": 4
            },
            "fields": {
                "value": float(data[6])
            }
        },
        {
            "measurement": "temperature",
            "tags": {
                "pi": hostname,
                "channel": 4
            },
            "fields": {
                "value": float(data[7])
            }
        }
    ]

    # start influx session and upload
    try:
        client = InfluxDBClient(server, influx_port, user, passwd, db)
        result = client.write_points(json_body)
        client.close()
        print("Result: {0}".format(result))
    except:
        print('Error connecting/uploading to InfluxDB')


# loop forever
while True:
     # this will log data every second
    for i in range(0,60):

        flag = None
        while flag is None:     # keep trying to match seconds with real time
            dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            second = datetime.now().strftime("%S")

            if int(second) == i:
                flag = 1
                break
            else:
                time.sleep(0.5)
                pass

        if int(second) == 0 and flag == 1:
            logdata(dt)     # save to SD card & upload
        else:
            pass

        time.sleep(0.1) # sleep script so the CPU is not bogged down
