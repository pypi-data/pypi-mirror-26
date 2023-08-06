pyesp included:
pyesp - command line tool

example 1: $ pyesp --help
--- display help for pyesp tool

example 2: $ pyesp --platform MPY --command listdir
--- Listed files/directories on EPS8266 file system

example 3: $ pyesp -p MPY -c listdir -d example
--- Listed files/directories on EPS8266 file system from './example' directory

example 4: $ pyesp -p MPY -c fileread -f sht21.py
--- Read file 'sht21.py' from EPS8266 file system

example 5: $ pyesp -p MPY -c fileread -f main.py,sht21.py,lm75.py
--- Read files [ main.py, sht21.py, lm75.py ] from EPS8266 file system

example 6: $ pyesp -p MPY -c filewrite -f main.py --data  import os\r\n import machine
--- Create file 'main.py' on EPS8266 and write 'import os\r\n import machine
