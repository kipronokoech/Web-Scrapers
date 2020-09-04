import requests
from bs4 import BeautifulSoup as Soup
import random

def get_proxy():
	url = "https://www.sslproxies.org/"

	r = requests.get(url)

	soup = Soup(r.content,"lxml")

	proxies_table = soup.find("table", attrs={"class": "table"})

	proxies = list(map(lambda x:x.text,proxies_table.findAll("td")[::8]))
	ports = list(map(lambda x:x.text,proxies_table.findAll("td")[1::8]))

	return (list(zip(proxies,ports)))

s = get_proxy()


def proxy_request(request_type, url,**kwargs):
	# while 1:
		# try:
			# required = {"https": s[0]+":"+s[1]}
	
			# print(proxy)
	while 1:
		try:
			proxy = random.choice(s)
			proxy = {"https": proxy[0]+":"+proxy[1]}
			print(proxy)
			r3 = requests.request(request_type,url,proxies=proxy, timeout=5,**kwargs)
			print(proxy)
			break
		except:
			pass
			# except:
			# 	pass
	return r3
rr = proxy_request("get","https://www.youtube.com")

print(rr.text)

