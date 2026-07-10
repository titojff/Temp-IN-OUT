# Temp-IN-OUT
Temp-IN/OUT my house

I have one temperature/humidity sensor outside my house and one inside,
connected to a Raspberry Pi3, I use it to know when should
open all windows at my house in the summer.
I use SHT45 sensors, run the pi headless from my linux PC, the code 
is in python, and writes to one .xlsx file on the pi. I have a Python script
on the PC to read the last line of that file, every 5 minutes and produce the graph.

GRAPHING.py is to be runned on the linux PC, it reads the xlsx file on the pi and produces the graph
