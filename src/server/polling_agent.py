import requests 
import pandas as pd
from pprint import PrettyPrinter
import json2html
import time
from style import style

pp = PrettyPrinter(indent=2)
_host_dict = pd.read_csv('host_list.csv').transpose().to_dict()
hosts = [_host_dict[k] for k in _host_dict] 

while True:
    try:
        for host in hosts:
            hostname = host['host']
            port= int(host['port'])
            proto= host['protocol']
            resource=host['resource']
            print('requestung...')
            response = requests.get(f'{proto}://{hostname}:{port}/{resource}', verify=False)
            #pp.pprint(response.json())
            with open('dummy.html','w') as fp:
                content = f'''
                    <html>
                        <title> host utilization </title>
                        <body>
                            <h1> {hostname} </h1>
                            <hr>
                            {json2html.json2html.convert(json = response.json())}
                        </body>
                    </html>
                '''
                fp.write(content)
        print('waiting...')
        time.sleep(2)    
    except KeyboardInterrupt:
        break