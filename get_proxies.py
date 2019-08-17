"""Find 10 working HTTP(S) proxies and save them to a file."""

import asyncio
import json
import os
import requests
from proxybroker import Broker
import asyncio
import random
import ast

proxies_file_path = os.path.join(os.getcwd(),"data","proxies.txt")

my_proxy = []
async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'w') as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = 'https' if 'HTTPS' in proxy.types else 'http'
            row = '%s://%s:%d' % (proto, proxy.host, proxy.port)
            my_proxy = row
            
            my_data = {
                'proxy':row,
                'status':'not used'
            }
            f.write(json.dumps(my_data))
            f.write("\n")

def getProxies(n,typ):
    async def show(proxies):
        p = []
        while True:
                proxy = await proxies.get()
                if proxy is None: break
                p.append("{}://{}:{}".format(proxy.schemes[0].lower(), proxy.host, proxy.port))
        return p
    
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=[typ], limit=n), show(proxies))
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(tasks)[1]

def generate_proxies():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], limit=200),
                        save(proxies, filename=proxies_file_path))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


    # proxyPool = getProxies(n,typ)
    # random.shuffle(proxyPool)
    # for proxy in proxyPool:
    #     try:
    #         my_proxy.append(proxy)
    #         # print(proxy, requests.get("https://v4.ident.me/", proxies={"http": proxy, "https": proxy}).text.strip())
    #     except Exception as e:
    #         print(e)
    # if bool(my_proxy):
    #     return my_proxy
    # else:
    #     return generate_proxies(n)



# def getProxyDict():
#     pro =  generate_proxies(1,'HTTP')
#     pro_2 =  generate_proxies(1,'HTTPS')
#     proxy = {
#         'http':my_proxy[0],
#         'https':my_proxy[1]
#     }
#     return proxy

def get_proxy_list():

    # try:
    #     with open(proxies_file_path,'r') as f:
    #         if len(f.readlines()) < 10:
    #             print("\n[*] generating proxies ...")
    #             generate_proxies()
    #             print("[*] generating proxies Done.")
    #         f.close()
    # except Exception as e:
    #     print(e)
    #     generate_proxies()


    my_lst = []
    with open(proxies_file_path,'r') as f:
        for lines in f.readlines():
            if not bool(lines):
                continue
            dictionary = ast.literal_eval(lines)
            my_lst.append(dictionary)
        f.close()
    return my_lst


if __name__ == "__main__":
    print("\n[*] Generating Proxies...")
    generate_proxies()
