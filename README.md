# ev3db
EV3 debug bridge for ev3dev

This program simplifies the download, startup and execution of python programs on the ev3dev by leaving a process
always alive and forking it on a new program execution, instead of creating a new python process every time

## Installation
Just install the library from [Pypi](https://pypi.org/project/ev3db/) and run
```bash
ev3db-cli --setup
```
To install all the libraries on the ev3dev connected to your computer

## Usage

Just run
```bash
ev3db-cli <program folder or file>
```
The program will compress the folder or the file, send it to the ev3 by using a REST server, start it fast, show the
logs on your console and stop on keyboard interrupt or on the press of the ev3 stop button