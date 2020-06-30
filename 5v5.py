import requests
import json

if __name__ == '__main__':
    location = r'C:\Garena\Games\32775\LeagueClient\lockfile'
    config = json.dumps({
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
        lockfile = open(location, 'r')
        data = lockfile.readline().split(':')
        port, token, protocol = data[2:]
    except FileNotFoundError:
        print('Please open lol client')
    else:
        url = r'{}://riot:{}@127.0.0.1:{}/lol-lobby/v2/lobby'.format(protocol, token, port)
        response = requests.post(url, data=config, verify=False)
    finally:
        input('Press Enter to exit')
