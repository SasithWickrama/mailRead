import email
import os
import random
from urllib.parse import urlparse
import requests.adapters
import zeep
from cryptography.fernet import Fernet
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM, Q, HTMLBody
import pandas as pd

from log import getLogger
from sendsms import Sendsms

logger = getLogger('crmsms', 'logs/crmsms')

fernet = Fernet(b'FzCF6B9_NzAgKNByBJsWTuJ56Q2uZkFlg2VYlU1vn70=')
decMessage = fernet.decrypt(b'gAAAAABjGWz73ESCIKuBqCawVWHv5j7Xx6YhkJ1lbKCuPUy3VgeMdVliYsRrChZ9axipNfKOlw7uNhaH1Qfo9NzoiJmj9FlzFg==').decode()

class RootCAAdapter(requests.adapters.HTTPAdapter):
    """An HTTP adapter that uses a custom root CA certificate at a hard coded
    location.
    """

    def cert_verify(self, conn, url, verify, cert):
        cert_file = {
            'mail.slt.com.lk': 'D:\DevOps\Python\mailRead\mailcertificate.cer',
        }[urlparse(url).hostname]
        super().cert_verify(conn=conn, url=url, verify=cert_file, cert=cert)

#v8{xa2j<VGrc
# Use this adapter class instead of the default
# BaseProtocol.HTTP_ADAPTER_CLS = RootCAAdapter
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
creds = Credentials(
    username="crminfosms",
    password='6rT*&C243#'
)#Telecom@#7890

config = Configuration(server='mail.crm.slt.lk', credentials=creds)

account = Account(
    primary_smtp_address="crminfosms@crm.slt.lk",
    autodiscover=False,
    config=config,
    access_type=DELEGATE,
)

def specific_string(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))


for item in account.inbox.all().filter(is_read=False).order_by('-datetime_received')[
            :10]:
    ref = specific_string(15)
    print(item.subject,item.body)
    # logger.info(ref+" START ============================================================")
    # if str(item.subject)[0:2] == '07' and len(item.subject)== 10:
        # item.is_read = True
        # item.save()
        # item.delete()
        
        # logger.info(ref+" From : " + str(item.sender))
        # logger.info(ref+" Date : " + str(item.datetime_received))
        # logger.info(ref+" Mobile : "+item.subject)
        # logger.info(ref+" Message : "+item.body)
        # try:
            # Sendsms.sendSms(item.subject, item.body, 'OSS', ref)
        # except Exception as e:
            # logger.error(ref+" error : "+str(e))
    # else:
         # print("Invalid Mobile Number : " + str(item.subject))
         # item.is_read = True
         # item.save()
         # item.delete()
         # logger.info(ref+" From : " + str(item.sender))
         # logger.info(ref+" Date : " + str(item.datetime_received))
         # logger.info(ref+" Mobile : "+item.subject)
         # logger.info(ref+" Message : "+item.body)
         # logger.info(ref+" Invalid Mobile Number : " + str(item.subject))
    # logger.info(ref+" END ============================================================")