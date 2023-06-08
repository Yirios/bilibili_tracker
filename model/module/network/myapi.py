import requests
from module.tool import read_json


def get_up_stat(mid):
    url = f"https://api.bilibili.com/x/space/upstat?mid={mid}&jsonp=jsonp"
    headers = {
        'referer':
        'https://space.bilibili.com/14392124',
        'cookie':
        read_json('conf\Credential.json')['cookie'],
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'
    }
    rep = requests.get(url=url, headers=headers)
    data = rep.json()
    rep.close()
    return data


def get_space_notice(mid):
    url = f"https://api.bilibili.com/x/space/notice?mid={mid}&jsonp=jsonp"
    headers = {
        'referer':
        'https://space.bilibili.com/14392124',
        'cookie':
        read_json('conf\Credential.json')['cookie'],
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'
    }
    rep = requests.get(url=url, headers=headers)
    data = rep.json()
    rep.close()
    return data


if __name__ == '__main__':
    # print(get_up_stat(14392124))
    print(get_space_notice(14392124))