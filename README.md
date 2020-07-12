# t-watch-2020-micropython
Edit copy of @mooond's code ([source](https://gitlab.com/mooond/t-watch2020-esp32-with-micropython))

## Motivation
Until the original code author updates his code with the following, this repo contains minimal changes to make the original code work:
- Missing library (focaltouch.py?)
- Missing font file (font5x8.bin)

## Test
Execute the following from your micropython IDE command line (I use Visual Studio Code with [Pymakr](https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr) extension):
```
import lily
li=lily.LILY()
li.testimg()
```
