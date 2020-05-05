import requests
from hashlib import md5

name = "wangyiqing8866"
pwd = "wyq123456789".encode("utf8")
soft_id = "904829"
pwd_2 = md5(pwd).hexdigest()
base_params = {
        "user":name,
        "pass2":pwd_2,
        "softid":soft_id,
}
headers = {
        "Connection":"Keep-Alive",
        "User-Agent":"User-Agent:Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv 11.0) like Gecko"
}
with open("code.gif","rb") as f:
    img = f.read()

params = {
        "codetype":1902
}
params.update(base_params)
print(params)
files = {"userfile":("ccc.gif",img)}
response = requests.post('http://upload.chaojiying.net/Upload/Processing.php',data=params,files=files,headers=headers)
print(response.json())
