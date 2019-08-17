
""" author: awais
"""

import random
import mechanicalsoup
import string
import logging
import pycountry






#generating a username
def username(identity):
    n = str(random.randint(1,99))
    name = str(identity).lower().replace(" ","")
    username = name + n
    logging.info("Username: {}".format(username))
    return(username)


#generate password
def generatePassword():
    password_characters = string.ascii_letters + string.digits
    return ''.join(random.choice(password_characters) for i in range(12))


def genEmail(username) :
    email_domain = ['gmail.com','yahoo.com','outlook.com','hotmail.com']
    choosen_domain = email_domain[random.randint(0,len(email_domain)-1)]
    return ''.join(username + "@" + str(choosen_domain))

def new_account():
    account_info = {}
    identity, gender, birthday = getRandomIdentity()
    account_info["name"] = identity
    account_info["username"] = username(account_info["name"])
    account_info["password"] = generatePassword()
    account_info["email"] = genEmail(account_info["username"])
    account_info["gender"] = gender
    account_info["birthday"] = birthday
    return(account_info)

def get_country():
    countries = pycountry.countries
    countries = list(countries)
    choosen_country = countries[random.randint(0,len(countries)-1)]
    return choosen_country.name


def getRandomIdentity():
    country = None
    while country is None:
        country = get_country()
    gender = random.choice(["male", "female"])
    logging.info("Gender: {}".format(gender))
    URL = "https://it.fakenamegenerator.com/gen-{}-{}-{}.php".format(gender,country,country)
    logging.info("Url generated: {}".format(URL))
    browser = mechanicalsoup.StatefulBrowser(
        raise_on_404=True,
        user_agent='MyBot/0.1'
    )
    page = browser.get(URL)
    address_div = page.soup.find("div",{ "class": "address" })
    completename = address_div.find("h3")
    extra_div = page.soup.find("div",{ "class": "extra" })

    all_dl = page.soup.find_all("dl",{'class':'dl-horizontal'})

    birthday = all_dl[5].find("dd").contents[0]
    logging.info("Birthday: {}".format(birthday))

    return(completename.contents[0],gender, birthday)
