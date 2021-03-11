## InfoCollector

### requests

```shell script
pip install flask gevent requests
```

### usage 

for server node

```shell script
$ python main.py --help
usage: main.py [-h] [--port PORT] [--database DB_NAME]

optional arguments:
  -h, --help          show this help message and exit
  --port PORT         port for listening, default [3000]
  --database DB_NAME  sqlite3 database name, default [:memory:]
```

for device node

```
$ python report_ip.py  --service_ip SERVER_IP --service_port SERVER_PORT --device_name DEVICE_NAME
``` 

for requesting online devices, visit the website of `http://SERVER_IP:SERVER_PORT`
