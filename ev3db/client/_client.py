from typing import Any,Dict,Tuple
from os.path import basename
from ev3db.api import *
from base64 import b64encode
from ._requests import curl

def push(url:str,file:str)->str:
    return __request(url,PUSH,{PUSH_EXTRA_NAME:basename(file),PUSH_EXTRA_DATA:b64encode(open(file,'br').read()).decode()})

def install(url:str,file:str)->str:
    return __request(url, INSTALL, {INSTALL_EXTRA_NAME:file})

def run(url:str,package:str)->int:
    return int(__request(url, RUN, {RUN_EXTRA_NAME:package}))

def interrupt(url:str,pid:int=-1)->str:
    return __request(url,INTERRUPT,{INTERRUPT_EXTRA_PID:pid})

def kill(url:str,pid:int=-1)->str:
    return __request(url,KILL,{KILL_EXTRA_PID:pid})

def is_alive(url:str,pid:int=-1)->str:
    return __request(url,IS_ALIVE,{IS_ALIVE_EXTRA_PID:pid})

def logs(url:str,pid:int=-1)->str:
    return __request(url,LOGS,{LOGS_EXTRA_PID:pid})

def errors(url:str,pid:int=-1)->str:
    return __request(url,ERRORS,{ERRORS_EXTRA_PID:pid})

def __request(url:str,command:Tuple[str,str],data:Dict[str,Any]=None)->str:
    response=curl(command[1],url+command[0],data)
    return response
