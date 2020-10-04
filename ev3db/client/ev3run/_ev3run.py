from ev3db.client import push,install,logs,errors,is_alive,interrupt,kill
import ev3db.client
from sys import stderr
from time import sleep,time
from typing import List
from os import remove
from os.path import basename
import tarfile

def run(program:str,url:str='ev3dev.local',download_only:bool=False):
    target = program
    program = basename(program)
    if '.py' in program:
        program = program[:-3]
    file = program + '.ev3'
    with tarfile.open(file, 'w:gz') as f:
        f.add(target, basename(target))
    push(url, file)
    remove(file)
    install(url, file)
    if download_only:
        return
    pid=ev3db.client.run(url,program)
    out_err=[0,0]
    try:
        while is_alive(url) == 'TRUE':
            sleep(1)
            get_logs(url,pid,out_err)
    except KeyboardInterrupt:
        interrupt(url,pid)
    stop_time=time()+3
    while is_alive(url,pid) == 'TRUE':
        sleep(1)
        get_logs(url,pid,out_err)
        if time() > stop_time:
            kill(url,pid)
    get_logs(url,pid,out_err)

def get_logs(url:str,pid:int,out_err:List[int]):
    string = logs(url,pid)[out_err[0]:]
    out_err[0] += len(string)
    print(string, end='',flush=True)
    string = errors(url,pid)[out_err[1]:]
    out_err[1] += len(string)
    print(string, file=stderr, end='',flush=True)
