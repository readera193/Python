import requests
import json
import os
import traceback

# Ignore InsecureRequestWarning
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def main():
    lockfile_location = r'C:\Garena\Games\32775\LeagueClient\lockfile'
    lobby_json = json.dumps({
        "customGameLobby": {
            "configuration": {
                "gameMode": "PRACTICETOOL",
                "gameMutator": "",
                "gameServerRegion": "",
                "mapId": 11,
                "mutators": {
                    "id": 1,
                },
                "spectatorPolicy": "AllAllowed",
                "teamSize": 5,
            },
            "lobbyName": "196_practice",
            "lobbyPassword": None,
        },
        "isCustom": True,
    })
    try:
        with open(lockfile_location, 'r') as lockfile:
            data = lockfile.readline().split(':')
            port, token, protocol = data[2:]
            url = r'https://riot:{}@127.0.0.1:{}/lol-lobby/v2/lobby'.format(token, port)
            requests.post(url, data=lobby_json, verify=False)
    except FileNotFoundError:
        print('找不到 lockfile 檔案，請開啟 lol 客戶端')
    except Exception:
        print('不明的程式中斷')
        traceback.print_exc()
    else:
        print('執行成功')
        return
    finally:
        os.system('pause')

if __name__ == '__main__':
    main()