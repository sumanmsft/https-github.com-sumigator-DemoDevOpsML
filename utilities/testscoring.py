import requests

data = open('test-image/pepsi.jpg', 'rb').read()
res = requests.post(url='http://52.180.89.39:80/score',
                    data=data,
                    headers={'Content-Type': 'application/octet-stream'})
print(res)