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
        print(f"[#] Login failed: {e}")  # For debug
        return None


def changeSpeed(speed, qbt_client):
    print(
        f"[#] Changing global down speed to {int(speed)} Bytes/s ({int(speed / 1048576)} MB/s)"
    )  # For debug
    for torrent in qbt_client.torrents_info():
        torrent.download_limit = int(speed)


def apps(speed, appName, qbt_client):  # --apps
    limited = False

    print(f"[#] Checking for proccess {appName}.exe")  # For debug
    while True:
        if f"{appName}.exe" in (i.name() for i in psutil.process_iter()):
            print("[#] Proccess alive")  # For debug
            if limited == False:
                changeSpeed(speed, qbt_client)
                limited = True
                for torrent in qbt_client.torrents_info():
                    previousNum = torrent.download_limit
                    if previousNum == 0:
                        previous = "Inf"
                    else:
                        previous = previousNum / 1048576
                    if speed == 0:
                        print(
                            f"[-] Previous download limit was {previous} MB/s but is now Inf MB/s || {torrent.name}"
                        )  # For debug
                    else:
                        print(
                            f"[-] Previous download limit was {previous} MB/s but is now {speed / 1048576} MB/s || {torrent.name}"
                        )  # For debug
                time.sleep(5)

        else:
            print("[#] Proccess not found")  # For debug
            if limited == True:
                changeSpeed(0, qbt_client)
                limited = False
            time.sleep(5)


def appList(speed, applications, qbt_client):  # --list
    limited = ""
    print("[#] Now in list mode")
    while True:
        for app in applications:
            # print(f'[#] Checking for proccess {app}.exe') # For debug

            if f"{app}.exe" in (i.name() for i in psutil.process_iter()):
                print(f"[✓] Proccess {app}.exe alive")  # For debug
                # print(limited) # For debug

                changeSpeed(speed, qbt_client)
                limited = f"{app}True"  # Set var limited to apps name and true so speed wont be effected by status of other apps
                time.sleep(0.75)  # Reduce load

            else:
                # print(f'[✘] Proccess {app}.exe not found') # For debug
                # print(limited) # For debug
                if limited == f"{app}True":
                    changeSpeed(0, qbt_client)
                    limited = f"{app}False"  # Set var limited to apps name and false so speed wont be effected by status of other apps
                time.sleep(0.75)  # Reduce load


def downloads(qbt_client):
    for torrent in qbt_client.torrents_info(
        status_filter="downloading", sort="priority"
    ):
        # torrent.download_limit = int(speed)
        if torrent.download_limit == 0.0 or 0:
            down = "Inf"
        else:
            down = round(torrent.download_limit / 1048576, 2)

        if torrent.upload_limit == 0.0 or 0:
            up = "Inf"
        else:
            up = round(torrent.upload_limit / 1048576, 2)

        print(
            f"[{torrent.priority:<2n}] - {torrent.name:<90s}    [ Down Limit: {(str(down) + " MB/s ]"):^13s} [ Up Limit: {(str(up) + " MB/s ]"):^13s}  [ Size: {(str(round(torrent.size/1073741824)) + "GB ]"):^9s} [ Seeds: {torrent.num_seeds:^3n} ]    [ Category: {torrent.category} ]    [ Time Left: {(str(round((torrent.eta/60)/60)) + " Hours" ):^12s}]"
        )


def manual(qbt_client, usage):
    speed = float(
        input("[#] What would you like to change the speed to? (MB/s)\n[#] 0 for Inf\n")
    )  # Manual change (no args)
    if speed != None:
        changeSpeed(speed * 1048576, qbt_client)
    else:
        print(usage)


def main():
    conn_info = dict(
        host="x.x.x.x",  # Ip of qBittorrent WebUI
        port=8080,  # port of qBittorrent WebUI
        username="admin",  # User
        password="1234",  # Passwd
    )

    # applications = ['r5apex', 'cs2', 'bfv', 'TslGame', 'Rounds', 'Terraria', 'RobloxPlayerBeta'] # Change / add any of these to be the name of the executables that you want to detect
    applications = ["Notepad", "notepad++"]  # For debug
    listSpeed = 0.3  # Change to whatever speed you want your torrents to be while any of the apps are detected
    usage = f"Usage: python3 {sys.argv[0]} [Options]\n\n--apps [name] [speed]\n   Auto changes torrent speed based on if app is open\n\n--downloads\n   Shows current downloading torrents\n\n--list\n   Same as apps but uses hard coded list of apps\n\n--help\n   Shows this menu"

    qbt_client = connect_to_qbittorrent(conn_info)

    if qbt_client:  # Only run if connected to WebUI succesfully
        if len(sys.argv) >= 2:
            if sys.argv[1] == "-d" or sys.argv[1] == "--downloads":
                downloads(qbt_client)
            elif sys.argv[1] == "--list" or sys.argv[1] == "-l":
                appList(listSpeed * 1048576, applications, qbt_client)
            elif sys.argv[1] == "--single" or sys.argv[1] == "-s":
                try:
                    apps(float(sys.argv[2]) * 1048576, sys.argv[3], qbt_client)
                except IndexError as e:
                    print(usage)
            else:
                print(usage)

        else:
            manual(qbt_client, usage)

        qbt_client.auth_log_out()


if __name__ == "__main__":
    main()
