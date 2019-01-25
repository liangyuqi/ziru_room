import requests

proxy = {'http': 'http://117.85.105.170:808',
         'https': 'https://117.85.105.170:808'}

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Connection': 'keep-alive'}

p = requests.get('http://icanhazip.com', headers=head, proxies=proxy)

print(p.text)
