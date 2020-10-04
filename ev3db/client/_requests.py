from subprocess import Popen,PIPE
from typing import Dict
from json import dumps

def curl(method:str,url:str,data:Dict)->str:
    process = Popen(['curl','--silent','--output','/dev/stderr','--write-out','%{http_code}','-X',method,'-d',dumps(data),url], stdout=PIPE, stderr=PIPE)
    result = process.stderr.read().decode()
    code=int(process.stdout.read().decode())
    if code==0:
        raise Exception('Can\'t connect to {}'.format(url))
    elif code != 200:
        raise Exception('Error code {}: {}'.format(code,result))
    return result
