import config
import ids
from simple_salesforce import Salesforce, SFType, SalesforceLogin
import sys

'''This is a salesforce sandbox clearing file that deletes whatever fields I 
need it to delete'''


session_id, instance = SalesforceLogin(
    username=config.username, password=config.password, security_token=config.token, sandbox=True)
sf = Salesforce(instance=instance, session_id=session_id)


contact_query = "Select Id, Name from Contact"
non_test_query = "SELECT Name, Id FROM Opportunity WHERE not (Name like 'Test%')"
opp_owner = "SELECT OwnerId FROM Opportunity"
contacts = sf.query(query=contact_query)
opportunities = sf.query(query=non_test_query)

print('''Do you want to delete:
1. Opportunities
2. Contacts
3. Exit''')
select = int(input('Selection: '))
if select == 1:
    print('Deleting Opportunities...')
    for record in opportunities['records']:
        id = record['Id']
        sf.Opportunity.delete(id)

elif select == 2:
    print('Deleting Contacts...')
    for record in contacts['records']:
        id = record['Id']
        sf.Contact.delete(id)

else:
    print('Bye Bye')
    # sys.exit()
