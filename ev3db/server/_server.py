from ev3db import VERSION
from ev3db.api import *
from typing import Tuple,Union
from base64 import b64decode
from os import getcwd,kill,remove,makedirs,getpid,listdir,system
from os.path import exists,join,basename
from signal import SIGINT,SIGKILL
from select import select
import sys
from importlib import import_module
from multiprocessing import Process
from subprocess import Popen, PIPE
from threading import Thread
from typing import Optional
from time import time
import tarfile
import ev3db.server._restful_server
from ._restful_server import HttpCode
local='ev3dev' not in Popen(['uname','-a'], stdout=PIPE).stdout.read().decode()
if not local:
    from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, DeviceNotDefined
    from ev3dev2.button import Button

    # Imports to speed up program startup
    CACHE_MODULES=['ev3dev2.motor', 'ev3dev2.button', 'ev3dev2.wheel', 'ev3dev2.port', 'ev3dev2.display',
                   'ev3dev2.auto', 'ev3dev2.console', 'ev3dev2.led', 'ev3dev2.power', 'ev3dev2.sound',
                   'ev3dev2.stopwatch', 'ev3dev2.unit', 'ev3dev2.version', 'ev3dev2.sensor.lego', 'ev3dev2.fonts',
                   'traceback','time']
    for cache_module in CACHE_MODULES:
        import_module(cache_module)

sys.path.append(getcwd())

processes=set()
running=True
OK='OK'
Return=Union[str,Tuple[str,int]]
input_lock=None  # type: Optional[Process]

def run(port:int=55555):
    global running
    print(' * Local mode:','on' if local else 'off')
    Thread(target=button_interrupt).start()
    commands = {HELLO: hello,
                PUSH:push,
                INSTALL:install,
                RUN:run_module,
                INTERRUPT:interrupt,
                KILL:kill,
                IS_ALIVE:is_alive,
                LOGS:logs,
                ERRORS:errors}
    try:
        ev3db.server._restful_server.run(port,commands)
    except BaseException as e:
        running=False
        raise e

def button_interrupt():
    if local:
        button=None
    else:
        button=Button()
    while running:
        if local:
            while running:
                i, o, e = select([sys.stdin], [], [], 0.1)
                if i and sys.stdin.readline().strip()=='b':
                    break
        else:
            while running:
                button.wait_for_pressed(['backspace'],1000)
                if button.backspace:
                    break
        send_signal(SIGINT, -1,False)
        end=time()+3
        while len(processes)>0:
            update_processes()
            if time()>end:
                send_signal(SIGKILL,-1,False)

def hello()->str:
    return 'ev3db {}'.format(VERSION)

def push(name,data)-> Return:
    data=b64decode(data)
    with open(name,'wb') as f:
        f.write(data)
    return name

def install(name)-> Return:
    file=name
    if not exists(file):
        raise HttpCode(404,'File {} not found'.format(file))
    package=file.split('-')[0]
    with tarfile.open(file,'r') as f:
        f.extractall()
    remove(file)
    return package

def run_module(name)->Return:
    global input_lock
    module=name
    if not exists(module) and not exists(module+'.py'):
        raise HttpCode(404,'Program {} not found'.format(module))
    makedirs('.logs',exist_ok=True)
    for file in listdir('.logs'):
        if 'err' in file:
            continue
        should_remove=True
        pid=int(basename(file)[:-8])
        for process in processes:
            if process.pid==pid:
                should_remove=False
                break
        if should_remove:
            remove(get_log(pid,False))
            remove(get_log(pid,True))
    if not local:
        input_lock = Popen(['brickrun', 'sleep', 'infinity'])
    process=Process(target=start_module,args=(module,),name=module)
    process.start()
    Thread(target=handle_process, args=[process]).start()
    update_processes()
    processes.add(process)
    return str(process.pid)

def start_module(package:str):
    pid=getpid()
    sys.stdout = BufferedOut(open(get_log(pid,False), 'w'),sys.stdout)
    sys.stderr = BufferedOut(open(get_log(pid,True), 'w'),sys.stderr)
    system('beep')
    module= import_module(package)
    if hasattr(module, '__main__') and callable(module.__main__):
        module.__main__()

def get_log(pid:int,err:bool)->str:
    files={False:'out',True:'err'}
    return join('.logs', '{}_{}.txt'.format(pid,files[err]))

def handle_process(process:Process):
    global input_lock
    while running:
        process.join(1)
        if not process.is_alive():
            break
    if input_lock is not None:
        input_lock.terminate()
        input_lock=None
    stop_all()

def stop_all():
    if local:
        print('Stop all')
    else:
        outputs = [OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D]
        for output in outputs:
            try:
                motor = Motor(output)
                motor.reset()
            except DeviceNotDefined:
                pass


class BufferedOut:
    def __init__(self,stream1,stream2):
        self.stream1=stream1
        self.stream2=stream2

    def write(self,data):
        self.stream1.write(data)
        self.stream2.write(data)
        self.stream1.flush()
        self.stream2.flush()

    def flush(self):
        self.stream1.flush()
        self.stream2.flush()

def update_processes():
    global processes
    dead=set()
    for process in processes:
        if not process.is_alive():
            dead.add(process)
    processes=processes-dead

def interrupt(pid)->Return:
    return send_signal(SIGINT,pid)

def kill_process(pid)->Return:
    return send_signal(SIGKILL,pid)

def send_signal(signal:int,pid:int,exception:bool=True)-> Return:
    update_processes()
    ok=False
    for process in processes:
        if pid==-1 or pid==process.pid:
            kill(process.pid, signal)
            ok=True
    # stop_all()
    if not ok and exception:
        raise HttpCode(404,'Pid {} not found'.format(pid))
    return OK

def is_alive(pid)->Return:
    update_processes()
    ok=False
    for process in processes:
        if pid==-1 or process.pid==pid:
            ok=True
            break
    return str(ok).upper()

def logs(pid)->Return:
    content=''
    if pid==-1:
        for file in listdir('.logs'):
            if 'out' in file:
                content+=open(join('.logs',file)).read()
    else:
        file=get_log(pid,False)
        if exists(file):
            content+=open(get_log(pid,False)).read()
    return content

def errors(pid)->Return:
    content= ''
    if pid == -1:
        for file in listdir('.logs'):
            if 'err' in file:
                content += open(join('.logs', file)).read()
    else:
        content += open(get_log(pid, True)).read()
    return content

if __name__=='__main__':
    run()
