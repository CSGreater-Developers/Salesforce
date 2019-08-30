import config
import csv
import ids
import os
from simple_salesforce import Salesforce, SFType, SalesforceLogin
import sys
import time


session_id, instance = SalesforceLogin(
    username=config.username, password=config.password, security_token=config.token, sandbox=True)
sf = Salesforce(instance=instance, session_id=session_id)


def formatDate(date):
    ref_date = date.split('/')
    ref_date = f'{ref_date[2]}-{ref_date[0].zfill(2)}-{ref_date[1].zfill(2)}'
    return ref_date


def getNames():
    records = sf.Opportunity.metadata()['recentItems']
    names = [name['Name'] for name in records]
    return names


def addContact():
    required_fields = ['FirstName', 'LastName', 'Email']
    print(
        f'Required Fields: {required_fields[0]}, {required_fields[1]}, {required_fields[2]}')
    fn = input('Enter the first name of the contact: ')
    ln = input('Enter the last name of the contact: ')
    email = input('Enter an email for the contact: ')

    print('Attempting to add contact')
    try:
        sf.Contact.create({
            required_fields[0]: fn,
            required_fields[1]: ln,
            required_fields[2]: email
        })
        print(f"Added Contact {fn} {ln} with email {email}\n")
    except Exception as e:
        error = e.content[0]['errorCode'].replace('_', ' ').title()
        print(f'Failed to add Contact: {error}\n')


"""
Enter the name of the Clinic: Tim Chen CS 2020
Enter the Stage Name for the Clinic: Brand New
Enter the Close Date for the Clinic: 2019-12-13
Enter the Academic Year for the Clinic: 2019-2020
Attempting to add Tim Chen CS 2020 Clinic
"""


def addOpportunity():
    required_fields = ['Name', 'StageName', 'CloseDate', 'Academic_Year__c']
    name = input('Enter the name of the Clinic: ')
    sn = input('Enter the Stage Name for the Clinic: ')
    cd = input('Enter the Close Date for the Clinic (yyyy-mm-dd): ')
    ay = input('Enter the Academic Year for the Clinic: ')
    # own = input('Who owns this: ')

    print(f"Attempting to add {name} Clinic")
    try:
        sf.Opportunity.create({
            required_fields[0]: name,
            required_fields[1]: sn,
            required_fields[2]: cd,
            required_fields[3]: ay,
        })
        print('Added Clinic successfully\n')
    except Exception as e:
        error = e.content[0]['errorCode'].replace('_', ' ').title()
        print(f'Failed to add {name} Clinic: {error}')


def addContactCSV():
    files = [f for f in os.listdir('./csvs/contacts') if os.path.isfile(
        os.path.join('./csvs/contacts', f))]
    print('\nCurrent files: ')
    for index, file in enumerate(files, start=1):
        print(f'{index}. {file}')
    f_select = int(input('\nWhich file would you like to open: '))
    selected_file = files[f_select-1]
    with open(f'./csvs/contacts/{selected_file}') as csvfile:
        cread = csv.reader(csvfile)
        next(cread)

        for row in cread:
            fn = row[1]
            ln = row[0]
            email = row[9]
            title = row[3]

            print('Attempting to add contact')
            try:
                sf.Contact.create({
                    'FirstName': fn,
                    'LastName': ln,
                    'Email': email,
                    'Title': title
                })
                print(f"Added Contact {title} {fn} {ln} with email {email}\n")
            except Exception as e:
                error = e.content[0]['errorCode'].replace('_', ' ').title()
                print(
                    f"Could not add {fn} {ln}: {error}.\n")


def addOpportunityCSV():
    files = [f for f in os.listdir('./csvs/clinics') if os.path.isfile(
        os.path.join('./csvs/clinics', f))]
    print('\nCurrent files: ')
    for index, file in enumerate(files, start=1):
        print(f'{index}. {file}')
    f_select = int(input('\nWhich file would you like to open: '))
    selected_file = files[f_select-1]
    with open(f'./csvs/clinics/{selected_file}') as csvfile:
        cread = csv.reader(csvfile)
        next(cread)

        names = getNames()

        for row in cread:
            year = row[0]
            # categ = row[1]
            sponser = row[2]
            # title = row[3]
            # liason = row[4]
            advisor = row[5].split(',')[0]
            # consultant = row[6]
            # students = row[7]
            desc = row[8]
            stage = row[9]
            cd = formatDate(row[10])
            # year_abv = row[11]
            # name_space = row[12]
            # year_space = row[13]
            # name_year = row[14]
            fullname = row[15]
            dept = row[16]
            ownerId = ''
            if advisor in ids.nameToID.keys():
                ownerId = ids.nameToID[advisor]
            else:
                ownerId = ids.nameToID['Colleen Coxe']

            print(f'Attempting to add {sponser} Clinic')

            if fullname in names:
                print(f'Failed to add {sponser} Clinic: Duplicates Detected\n')
                time.sleep(.1)
                continue

            try:
                sf.Opportunity.create({
                    'Name': fullname,
                    'StageName': stage,
                    'CloseDate': cd,
                    'Academic_Year__c': year,
                    'Description': desc,
                    'Department_s__c': dept,
                    'OwnerId': ownerId
                })
                print(f'Added {sponser} Clinic successfully\n')
                names.append(fullname)
            except Exception as e:
                error = e.content[0]['errorCode'].replace('_', ' ').title()
                print(f'Failed to add {sponser} Clinic: {error}')


def printMenu():
    message = '''What would you like to do:
    1. Create a contact?
    2. Create an opportunity?
    3. Read in a Contact CSV?
    4. Read in an Opportunity CSV?
    5. Quit
    '''
    print(message)


def main():
    print('Welcome to the Harvey Mudd Salesforce App')

    select = 0
    while select != 5:
        print('\n')
        printMenu()
        select = int(input('Selection: '))
        if select == 1:
            addContact()
        if select == 2:
            addOpportunity()
        if select == 3:
            addContactCSV()
        if select == 4:
            addOpportunityCSV()
        if select == 5:
            print('\nThank you for using this custom app')
            sys.exit()


if __name__ == "__main__":
    main()
