# Made by Sudo
# Discord: sudoxyz
# Email: sudo404xyz@gmail.com

import qbittorrentapi
import sys
import psutil 
import time

def connect_to_qbittorrent(conn_info):
    try:
        qbt_client = qbittorrentapi.Client(**conn_info)
        qbt_client.auth_log_in()
        return qbt_client
    except qbittorrentapi.LoginFailed as e:
        print(f"[#] Login failed: {e}") # For debug
        return None
    
def changeSpeed(speed, qbt_client):
    print(f"[#] Changing global down speed to {int(speed)} Bytes/s ({int(speed / 1048576)} MB/s)") # For debug
    for torrent in qbt_client.torrents_info():
        previousNum = torrent.download_limit
        if previousNum == 0:
            previous = 'Inf'
        else:
            previous = previousNum / 1048576
            
        torrent.download_limit = int(speed)
        if speed == 0:
            print(f"[-] Previous download limit was {previous} MB/s but is now Inf MB/s || {torrent.name}") # For debug
        else:
            print(f"[-] Previous download limit was {previous} MB/s but is now {speed / 1048576} MB/s || {torrent.name}") # For debug
            
def apps(speed, appName, qbt_client): # --apps
    limited = False
    
    print(f'[#] Checking for proccess {appName}.exe') # For debug
    while True:
        if f"{appName}.exe" in (i.name() for i in psutil.process_iter()):
            print('[#] Proccess alive') # For debug
            if limited == False:
                changeSpeed(speed, qbt_client)
                limited = True
            time.sleep(5)
            
        else:
            print('[#] Proccess not found') # For debug
            if limited == True:
                changeSpeed(0, qbt_client)
                limited = False
            time.sleep(5)
            
def appList(speed, applications, qbt_client): # --list
    limited = ''
    while True:
        for app in applications:
            print(f'[#] Checking for proccess {app}.exe') # For debug

            if f"{app}.exe" in (i.name() for i in psutil.process_iter()):
                print('[#] Proccess alive') # For debug
                print(limited) # For debug

                changeSpeed(speed, qbt_client)
                limited = f'{app}True' # Set var limited to apps name and true so speed wont be effected by status of other apps
                time.sleep(1) # Reduce load
            
            else:
                print('[#] Proccess not found') # For debug
                print(limited) # For debug
                if limited == f'{app}True':
                    changeSpeed(0, qbt_client)
                    limited = f'{app}False' # Set var limited to apps name and false so speed wont be effected by status of other apps
                time.sleep(1) # Reduce load
    

def main():
    conn_info = dict(
        host="192.168.0.223", # Ip of qBittorrent WebUI
        port=8080, # port of qBittorrent WebUI
        username="admin", # User
        password="ethan404", # Passwd
    )
    
    # applications = ['r5apex', 'cs2', 'bfv', 'TslGame', 'Rounds', 'Terraria'] # Change / add any of these to be the name of the executables that you want to detect
    applications = ['Notepad', 'notepad++'] # For debug
    listSpeed = 0.3 # Change to whatever speed you want your torrents to be while any of the apps are detected

    qbt_client = connect_to_qbittorrent(conn_info)

    if qbt_client: # Only run if connected to WebUI succesfully
        if len(sys.argv) >= 2:
            if sys.argv[1] == '--apps':
                apps(float(sys.argv[2])*1048576, sys.argv[3], qbt_client)
            elif sys.argv[1] == '--list':
                appList(listSpeed * 1048576, applications, qbt_client)
            else:
                print(f'Usage: python3 {sys.argv[0]} [Options]\n\n--apps [name] [speed]\n   Auto changes torrent speed based on if app is open\n\n--list\n   Same as apps but uses hard coded list of apps\n\n--help\n   Shows this menu')
                
        else:
            speed = float(input("[#] What would you like to change the speed to? (MB/s)\n[#] 0 for Inf\n")) # Manual change (no args)
            changeSpeed(speed*1048576, qbt_client)
            
        qbt_client.auth_log_out()


if __name__ == "__main__":
    main()