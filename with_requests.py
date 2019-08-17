import time
import os
import random
import requests
import re
import ssl
import json

from fake_account_generator import new_account
from get_proxies import generate_proxies,get_proxy_list
# from get_driver import get_header

# from hide_identity import get_hidden_session


from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

data_dir_path = os.path.join(os.getcwd(),'data')
users_file = os.path.join(data_dir_path,'usernames_passwords.txt')
proxies_file = os.path.join(data_dir_path,'proxies.txt')
cerificate_file = os.path.join(data_dir_path,'my_certificate.crt')


# proxy_list = get_proxy_list()


class request_creator():
    # s = get_hidden_session()
    s = requests.session()
    def __init__(self):
        self.account_info = new_account()
        self.user_name = self.account_info['username']
        self.password = self.account_info['password']
        self.email = self.account_info['email']
        self.fullname = self.account_info['name']
        self.gender = self.account_info["gender"]
        self.birthday = self.account_info["birthday"]
        self.i_created = False        
        self.crfs = None
        self.c_id = None



        self.url = "https://www.instagram.com/accounts/web_create_ajax/"
        self.referer_url = "https://www.instagram.com/"


        self.s.headers['x-requested-with'] = 'XMLHttpRequest'
        self.s.headers['Referer'] = 'https://www.instagram.com'
        self.s.headers['Origin'] = 'https://www.instagram.com'
        self.s.cookies['ig_cb'] = '1'

        # self.s.headers = {
		# 	'accept-encoding': 'gzip, deflate, br',
		# 	'accept-language': 'en-US,en;q=0.9',
		# 	'Referer': 'https://www.instagram.com',
		# 	'Origin': 'https://www.instagram.com',
		# 	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A402 Safari/604.1',
        #     'Accept': '*/*',
        #     'x-requested-with': 'XMLHttpRequest',
        # }
        # self.s.proxies = self.pick_proxy()
        try: 
            f = self.s.get('https://www.instagram.com/web/__mid/')
            print(self.s.cookies)
            try:
                self.crfs = self.s.cookies['csrftoken']
            except Exception as e:
                print(e)
            try:
                self.c_id = self.s.cookies['mid']
            except Exception as e:
                print(e)
            self.i_created = True
        except Exception as e:
            print("[!] internet connection or proxy fault",e)



    def new_account(self):
        print("\n[*] Generating Fake User Data ....")
        self.account_info = new_account()
        self.user_name = self.account_info['username']
        self.password = self.account_info['password']
        self.email = self.account_info['email']
        self.fullname = self.account_info['name']
        self.gender = self.account_info["gender"]
        self.birthday = self.account_info["birthday"]
        # self.s.headers = self.update_header()
        # self.s.proxies = self.pick_proxy()

    def update_header(self):
        return get_header()
        # self.s.headers['User-Agent'] = gen['User-Agent']




    def update_whole_session(self):
        self.s = get_hidden_session()
        self.s.headers = {
			'Referer': 'https://www.instagram.com',
			'Origin': 'https://www.instagram.com',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.s.cookies['ig_cb'] = '1'




    def sign_up(self):
        print("[*] Signing Up user ....")
        # Account creation payload
        # payload = {
        #     'email': self.email,
        #     'password': self.password,
        #     'username': self.user_name,
        #     'first_name': self.fullname,
        #     'seamless_login_enabled' : '1',
        #     'tos_version' : 'row',
        #     'opt_into_one_tap' : 'false'
        # }

        # """
        #     Check if to use local ip address to create account, then create account based on the amount set in the config.py
        # """
        # session = get_hidden_session()
        # print(session.get("http://httpbin.org/ip").text)
        # print(session.cookies)
        # try: 
        #     session_start = session.get(self.url)
            
        #     session.headers.update({'referer' : self.referer_url,'x-csrftoken' : session_start.cookies['csrftoken']})
        #     create_request = session.post(self.url, data=payload, allow_redirects=True)
        #     print(session.cookies)
        #     session.headers.update({'x-csrftoken' : session_start.cookies['csrftoken']})
        #     response_text = create_request.text
        #     response = json.loads(create_request.text)
        #     print(response)
        # except Exception as e:
        #     print(e)
        #     print("---Request Bot --- An error occured while creating account with local ip address")







        # if not bool(self.s.headers):
        #     self.s.headers = self.update_whole_session()
        self.s.headers['x-instagram-ajax'] = 'f4c28142cf13'
        self.s.headers['x-ig-app-id'] = '936619743392459'

        try:
            self.s.headers['x-csrftoken'] = self.s.cookies['csrftoken']
        except:
            self.s.headers['x-csrftoken'] = self.crfs
        # print(self.s.headers['x-csrftoken'])
        self.s.headers['referer'] = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
        self.s.headers['content-type'] = 'application/x-www-form-urlencoded'

        try:
            clientId =  self.s.cookies['mid'],
        except:
            clientId =  self.c_id,
        # print(clientId)
        data = {
            'email': self.email,
            'password': self.password,
            'username': self.user_name,
            'first_name': self.fullname,
            'client_id': clientId,
            'seamless_login_enabled': '1',
            'gdpr_s': '[0,2,0,null]',
            'tos_version': 'eu',
            'opt_into_one_tap': 'false'
        }
        res = self.s.post('https://www.instagram.com/accounts/web_create_ajax/',verify=False , data=data).json()
        # print(self.s.cookies)
        print(res)
        try:
            if(res['status'] == 'fail'):
                time.sleep(5)
                return False
        except:
            pass
        try:
            if res['account_created'] == 'True':
                return True
            else:
                return False
        except:
            pass
    


    def pick_proxy(self):
        print("[*] Change Proxies ....")
        proxy = {}
        ind = 0
        for pro in proxy_list:
            if len(proxy) == 2:
                break
            if pro['proxy'][0:5] == 'https' and pro['status'] == 'not used':
                try:
                    if proxy['https']:
                        pass
                except:
                    proxy['https'] = pro['proxy']
                    proxy_list[ind]['status'] = 'used'
            elif pro['proxy'][0:5] == 'http:' and pro['status'] == 'not used':
                try:
                    if proxy['http']:
                        pass
                except:
                    proxy['http'] = pro['proxy'] 
                    proxy_list[ind]['status'] = 'used'
            else:
                pass
            ind+=1
        if len(proxy)<2:
            print("[*] All or single type are completely used ")
            exit(1)
            # generate_proxies()
            # # return self.pick_proxy()
        
        print("[**] Using Proxy {}".format(proxy))
        return proxy






    def save_account_to_file(self):
        print("[*] Saving account to File ....")
        try:
            with open(users_file,'r') as f:
                f.close()
        except:
            with open(users_file,'w') as f:
                f.close()
        with open(users_file,'a') as f:        
            one_line = self.user_name+","+self.password+"\n"
            f.write(one_line)
            f.close()
        print("[*] Writing to File is Done !")

    def display_success(self):
        self.save_account_to_file()
        print("\n[**] ---- account created Successfully ---- ")
        print("[*] Username = {}".format(self.user_name))
        print("[*] password = {}".format(self.password))
        print("[*] email = {}".format(self.email))
        print("[*] full name = {}".format(self.fullname))
        print("[*] Gender = {}".format(self.gender))
        print("[*] Birthday = {}".format(self.birthday))
        print("\n")


if __name__ == "__main__":
    # b = request_creator()
    # b.new_account()
    # b.sign_up()
    bot = None
    while not bool(bot):
        bot = request_creator()
        if not bot.i_created:
            continue

    res = bot.sign_up()
    # while res is False:
    #     # bot.update_whole_session()
    #     bot.new_account()
    #     res = bot.sign_up()
    bot.display_success()