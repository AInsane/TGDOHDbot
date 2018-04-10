import requests
from requests.auth import HTTPBasicAuth
import config


tokenauth = config.auth_token
mailauth = config.auth_mail

# НЕ смог понять как импортировать модуль с указанием 'x <= знач ' через for in

def get_all_mails(usermail):

    x = 1
    resp = requests.get('https://support.abmcloud.com/api/v2/users/?page=%s' % (x),
                                 auth=HTTPBasicAuth(mailauth, tokenauth))
    respjson = resp.json()
    totalpages = respjson['pagination']['total_pages']
    #print(totalpages)

    while x <= totalpages:

        try:
            resp2 = requests.get('https://support.abmcloud.com/api/v2/users/?page=%s' % (x),
                                 auth=HTTPBasicAuth(mailauth, tokenauth))
            respjson2 = resp2.json()
            x = x + 1


            for i in range(0,30):
                response = respjson2['data'][i]['email']
                #print(response)
                if response == usermail:
                    return False

        except IndexError:
            print('КОНЕЦ СПИСКА Index Error')


#print(get_all_mails('a_roditeleva@mail.ru'))

if __name__=='__main__':
    get_all_mails()