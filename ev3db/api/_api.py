HELLO=('/','GET')

PUSH=('/push','POST')
PUSH_EXTRA_NAME='name'
PUSH_EXTRA_DATA='data'

INSTALL=('/install','POST')
INSTALL_EXTRA_NAME='name'

RUN=('/run','POST')
RUN_EXTRA_NAME='name'

INTERRUPT=('/interrupt','POST')
INTERRUPT_EXTRA_PID='pid'

KILL=('/kill','POST')
KILL_EXTRA_PID='pid'

IS_ALIVE=('/alive','GET')
IS_ALIVE_EXTRA_PID='pid'

LOGS=('/logs','GET')
LOGS_EXTRA_PID='pid'

ERRORS=('/errors','GET')
ERRORS_EXTRA_PID='pid'
