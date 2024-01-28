#!/bin/python3
import requests,os,re,sys,json,getpass
from template import build_readme

"""
CTFD Challenge Scrapper & Downloader
Fork of: https://github.com/bardiz12/ctfd-challenge-scraper
Modified by: https://github.com/Lobsterge/ctfd-challenge-scraper

Usage : python scraper.py [CTFD-URL] [output_dir] [USERNAME]"
"""
class Scraper():
    def __init__(self,base_url):
        self.user = {"username":None,"password":None}
        self.base_url = base_url[0:-1] if base_url[-1] == "/" else base_url
        self.request = requests.Session()

    def login(self,username,password):
        self.user['username'] = username
        self.user['password'] = password

        token = self.get_login_nonce()
        try_login = self.post("/login",{"name":username,"password":password,"nonce":token})
        if ("Your username or password is incorrect" in try_login.text):
            raise Exception('Wrong username/password')

    def get_login_nonce(self):
        page = self.get("/login")
        token = re.findall(r"<input id=\"nonce\" name=\"nonce\" type=\"hidden\" value=\"(.*?)\">",page.text)
        
        if token==[]:
            raise Exception('Could not get nonce token')
        return token[0]

    def get(self,path):
        return self.request.get(self.base_url  + path)

    def post(self,path,data):
        return self.request.post(self.base_url  + path,data)

    def apiGet(self,path):
        return self.get("/api/v1"+path)

    def download(self,directory_name):
        if os.path.isdir(directory_name):
            if os.path.isfile(directory_name):
                raise Exception(directory_name + " is not a valid directory")
        else:
            os.mkdir(directory_name)

        json_challs = self.apiGet('/challenges').text
        challenges = json.loads(json_challs)

        for chall in challenges['data']:
            
            if not chall["solved_by_me"]:
                continue

            id = chall["id"]
            name = chall["name"]
            category = chall["category"]

            print(f"[+] Downloading {name}, [{category}]")
        
            chall_info = json.loads(self.apiGet(f"/challenges/{id}").text)['data']
            description = chall_info["description"].replace("\r", "")
            files = chall_info["files"]
            connection_info = chall_info["connection_info"]
            
            chall_dir = directory_name + "/" + category + "/" + name
            os.makedirs(chall_dir)

            with open(chall_dir + "/README.md", "w") as output:
                output.write(build_readme(name, category, description, connection_info, files))
            
            for file_url in files:
                file_name = file_url.split("?token")[0].split("/")[-1]
                file_data = self.get(file_url).content
                file = open(chall_dir + "/" + file_name, "wb")
                file.write(file_data)
                file.close()
             
        print("[*] Done!")

def main():
    if(len(sys.argv) < 4):
        print("Usage: python3 scraper.py [CTFD-URL] [output_dir] [username]")
        exit()

    ctf_url = sys.argv[1]
    output_dir = sys.argv[2]
    username = sys.argv[3]
    password = getpass.getpass("Password: ")

    scraper = Scraper(ctf_url)
    print("[*] Starting scraping...")
    try:
        scraper.login(username,password)
    except Exception as e:
        print(f"[!] {e}")
        exit()
    scraper.download(output_dir)

if __name__ == "__main__":
    main()