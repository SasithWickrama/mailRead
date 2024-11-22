import email
import os
from urllib.parse import urlparse
import requests.adapters
import zeep
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from exchangelib import DELEGATE, Account, Credentials, Configuration, FileAttachment, ItemAttachment
import pandas as pd
from cryptography.fernet import Fernet

from log import getLogger

logger = getLogger('offnetmobitel', 'logs/offnetmobitel')

fernet = Fernet(b'il4gsK-SJ4PUeygJseQ7W7KJ7mbIFU6cePBa3DeAWYM=')
decMessage = fernet.decrypt(
    b'gAAAAABisrwT1wpAAhlM7MV3K-47SKvFyQZI92Bgp9By1pC572zk_aD-MI9R491h5OLee1cysVsrxE-bBIgA88K2UTiJWIIIxg==').decode()


class RootCAAdapter(requests.adapters.HTTPAdapter):
    """An HTTP adapter that uses a custom root CA certificate at a hard coded
    location.
    """

    def cert_verify(self, conn, url, verify, cert):
        cert_file = {
            'mail.slt.com.lk': 'D:\DevOps\Python\mailRead\mailcertificate.cer',
        }[urlparse(url).hostname]
        super().cert_verify(conn=conn, url=url, verify=cert_file, cert=cert)


#12Ont$!blc0175
# Use this adapter class instead of the default
# BaseProtocol.HTTP_ADAPTER_CLS = RootCAAdapter
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
creds = Credentials(
    username="offnetblock",
    password=decMessage
)

config = Configuration(server='mail.slt.com.lk', credentials=creds)

account = Account(
    primary_smtp_address="offnetblock@slt.com.lk",
    autodiscover=False,
    config=config,
    access_type=DELEGATE,
)

for item in account.inbox.all().filter(sender='bypasscontrol@mobitel.lk', is_read=False).order_by('-datetime_received')[
            :2]:
    print(item.subject, item.sender, item.datetime_received,item.attachments)

    for attachment in item.attachments:
        if os.path.exists("tcg.txt"):
            os.remove("tcg.txt")
            with open("tcg.txt", 'wb') as f:
                f.write(attachment.content)


    logger.info("START ============================================================")
    logger.info("From : " + str(item.sender))
    logger.info("Subject : " + str(item.subject))
    logger.info("Date : " + str(item.datetime_received))
    print(item.is_read)
    item.is_read = True
    item.save()
    item.delete()


    with open("tcg.txt", mode='r', encoding='utf-8') as tcg_file:
        for a_contact in tcg_file:
            numb = a_contact.split()[1]
            if numb[0:3] == '947' and len(numb) == 11:
                num = '0'+numb[2:]
                #print('0'+numb[2:])


                if str(num)[0:2] == '07' and len(num) == 10:
                    print(num)
                    logger.info("CLI Detected Calling Number : " + num)
                    try:
                        wsdl = 'http://172.25.37.196:8080/NSecurity/RService?wsdl'
                        client = zeep.Client(wsdl=wsdl)
                        result = client.service.TrunckNumberBkEn("HQ-IBCF", "3004", num, "ADD")
                        
                        if result == '0':
                            logger.info("RESULT HQ : " + result)
                            resultdr = client.service.TrunckNumberBkEn("WEL_IBCF", "3004", num, "ADD")
                            logger.info("RESULT WEL : " + resultdr)
                            print(resultdr)
                        else:
                            logger.info("RESULT HQ : " + result)
                            print(result)
                    except Exception as e:
                        print(str(e))

                else:
                    print("Invalid Mobile Number : " + str(num))
                    logger.info("Invalid Mobile Number : " + str(num))
    logger.info("END ============================================================")
