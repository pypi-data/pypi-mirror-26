## Dashbase Tools

### Install

```
pip install -e .
```

### logtail

Mimics a unix tail + grep combination and queries a dashbase service endpoint for aggregated logs.

#### Usage:
```
usage: logtail [-h] [-n NUM] -a ADDR [-q QUERY] [-t TIME]

Logtailer for Dashbase

optional arguments:
  -h, --help            show this help message and exit
  -n NUM, --num NUM     number of lines to return
  -a ADDR, --addr ADDR  Log address, e.g. table@host:port
  -q QUERY, --query QUERY
                        query string
  -t TIME, --time TIME  time filter, e.g. May 20 2017 10:11:13,10 min ago
```
  
example:
  
```
./logtail -n 5 -a dashbase-staging@staging.dashbase.io:9876 -t "May 20 2017 10:11:13,10 min ago" -q "linux AND NOT 200"
```
  
output:
```
start time: 2017-05-20 10:11:13
end time: 2017-05-20 18:52:51.719695
{'numResults': 5, 'table': ['dashbase-staging'], 'query': {'queryStr': 'linux AND NOT 200', 'queryType': 'string'}, 'disableHighlight': True, 'timeRangeFilter': {'endTimeInSec': 1495331571.0, 'startTimeInSec': 1495300273.0}}
found docs: 2,816,000,000 / 39,683,482,233
2017-05-20 18:52:50	{"request": "GET mobile.acme.com/mobile/data", "host": "236.44.91.53", "response": 500, "bytesSent": 4622, "agent": "Dalvik/2.1.0 (Linux; U; Android 5.0; vivo X5Pro D Build/LRX21M)"}
2017-05-20 18:52:50	{"request": "POST mobile.acme.com/mobile/data", "host": "224.230.119.3", "response": 408, "bytesSent": 329, "agent": "Dalvik/1.6.0 (Linux; U; Android 4.1.2; GT-S7572 Build/JZO54K)"}
2017-05-20 18:52:50	{"request": "POST mobile.acme.com/mobile/data", "host": "230.19.223.127", "response": 408, "bytesSent": 328, "agent": "Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-T311 Build/KOT49H)"}
2017-05-20 18:52:50	{"request": "POST mobile.acme.com/mobile/connect", "host": "70.204.122.91", "response": 401, "bytesSent": 726, "agent": "Dalvik/1.6.0 (Linux; U; Android 4.1.2; vivo Y11 Build/JZO54K)"}
2017-05-20 18:52:50	{"request": "POST mobile.acme.com/mobile/data", "host": "133.214.255.208", "response": 408, "bytesSent": 330, "agent": "Dalvik/1.6.0 (Linux; U; Android 4.0.3; HTC T328w Build/IML74K)"}
```

[![asciicast](https://asciinema.org/a/0xcdjcczhk7aannojcraai263.png)](https://asciinema.org/a/0xcdjcczhk7aannojcraai263)
  
### dbsql
  
  SQL command console for querying a dashbase service.
  
#### Usage:
  
  Just point to a Dashbase service url, e.g. ```staging.dashbase.io:9876```
  
  ```
  usage: dbsql [-h] -a ADDRESS [-o JSON]

  Sql console for Dashbase

  optional arguments:
    -h, --help            show this help message and exit
    -a ADDRESS, --address ADDRESS
                          Log name, e.g. host:port, required
    -o JSON, --output JSON  output in json format (true/false), default: false
  ```
      
example:
  
```
./dbsql -a staging.dashbase.io:9876
Starting Dashbase console...
> select * limit 1
+Hits-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+
| time                | RAW                                                                                                                                                         |
+---------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 2017-05-20 22:03:19 | {"request": "POST mobile.acme.com/mobile/data", "host": "68.251.31.64", "response": 200, "bytesSent": 940, "agent": "Dalvik/2.1.0 (Linux; U; Android 5.0.1; |
|                     | GT-I9500 Build/LRX22C)"}                                                                                                                                    |
+---------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------+
Time range: from 2017-05-20 21:49:47 to 2017-05-20 22:04:47
72,000,000 rows of 40,543,482,233 (0.01 sec)
>
```
[![asciicast](https://asciinema.org/a/2a4gczb7bm1mivh86dcmegdxw.png)](https://asciinema.org/a/2a4gczb7bm1mivh86dcmegdxw)
