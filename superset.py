import requests
from bs4 import BeautifulSoup
import os
import sys
import argparse
import os.path
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()



def grab_login(url):
	# Define the URL and headers for the login page
	login_url = ""+url+"/login/"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

	# Send a GET request to retrieve the login page
	res = session.get(login_url, headers=headers,verify=False)
	soup = BeautifulSoup(res.content, "html.parser")

	# Extract the CSRF token from the login page
	csrf_token = soup.find("input", {"name": "csrf_token"})["value"]

	# Define the payload for the POST request
	payload = {
    "csrf_token": csrf_token,
    "username": "admin",
    "password": "admin"
	}

# Send the POST request to the login URL with the payload
	res = session.post(login_url, data=payload, headers=headers, allow_redirects=True,verify=False)

	# Check if any redirect URL path contains "/superset/welcome/"
	redirected_urls = [res.url] + res.history
	if any("/superset/welcome/" in url for url in redirected_urls):
		print("Logged in - "+url+"")
		text_file = open("found.txt", "a")
		text_file.write(""+url+"\n")
		text_file.close()
	else:
		print("Login failed")



parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=False ,default="http://localhost",help="URL to test")
parser.add_argument("-f", "--file", default="",required=False, help="File of urls")
args = parser.parse_args()
url = args.url
urls = args.file





if urls:
	if os.path.exists(urls):
		with open(urls, 'r') as f:
			for line in f:
				url = line.replace("\n","")
				try:
					print("Testing "+url+"")
					grab_login(url)
				except KeyboardInterrupt:
					print ("Ctrl-c pressed ...")
					sys.exit(1)
				except Exception as e:
					print('Error: %s' % e)
					pass
		f.close()
	

else:
	grab_login(url)
