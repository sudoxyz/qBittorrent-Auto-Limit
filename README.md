# qBittorrent-Auto-Limit

I decided to make a program to solve an issue i was having, 
I have a very low bandwith and i was having problems gaming while torrenting on the same network due to the huge amount of ping. 
This python program uses the qBittorrent-api module to interact with the WebUI and change download speed limits whenever an executable from a set list is running. 


## Setup

- Change WebUI details
- Change items in list
- Change download speed limit
  
![image](https://github.com/user-attachments/assets/f41adabb-cf8c-4cff-b0c5-91aedb06d7bc)


## Usage
```
python3 autolimit.py [Options]
```
```
--apps [speed] [name]
    run the program to look for a single app 
```
```
--list
    run the program to look for all apps in the list
```
```
--help
    Shows help menu
```
Running with no args will default to the manual mode

## Example

```
python3 autolimit.py --apps 1 Notepad
```
This will look for Notepad. If its found the download speed will be limited to 1mb/s

