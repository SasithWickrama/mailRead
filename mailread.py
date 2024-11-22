from exchangelib import DELEGATE, Account, Credentials, Configuration,NTLM

creds = Credentials(
    username="012583@intranet.slt.com.lk", 
    password="AAdp@19870120"
)

config = Configuration(server='mail.slt.com.lk', credentials=creds)

account = Account(
    primary_smtp_address="prabodha@slt.com.lk",
    autodiscover=False, 
    config=config,
    access_type=DELEGATE
)

for item in account.inbox.all().order_by('-datetime_received')[:1]:
    print(item.subject, item.sender, item.datetime_received, item.body)