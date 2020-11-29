"""
Its simple Contact Book
for task of 'A Byte of Python'

You can Add/Edit/Delete/Search your contact
from simple DB.

Please test it...

Enjoy ;)
"""

import os
import pickle


def menu() -> 'actions':
    '''Function return start menu'''
    labels = [['name', 15], ['age', 6], ['email', 10], ['comment', 25]]

    exit = False
    while not exit:

        db_data = read_db()
        count_address = len(db_data)

        print(f'Total contacts - {count_address}')
        print('''
Please choise action:

        [1] - Open Contact Book
        [2] - Search Contact
        [3] - Add Contact
        [4] - Edit Contact

        [x] - Close Contact Book
        ''')

        action = input('Action: ')
        if action == '1':
            view_contacts(db_data, labels)
        elif action == '2':
            search_contact(db_data, labels)
        elif action == '3':
            action_contact(labels, db_data)
        elif action == '4':
            edit_contact(db_data, labels)
        elif action == 'x':
            exit = True
            print('Bye Bye!')
        else:
            print(f'"{action}" is not support now')


def check_db(db_name: str) -> str:
    '''Function check if DB is exist.
    If not exist, function creat DB'''

    db_path = 'db' + os.sep + db_name + '.data'

    if not os.path.isdir('db'):
        os.mkdir('db')
    if not os.path.isfile('db' + os.sep + db_name + '.data'):
        print(f'*** New DB - "{db_name}" is create! ***')
        with open('db' + os.sep + db_name + '.data', 'xb') as file:
            pickle.dump([], file)

    return db_path


def read_db() -> list:
    '''Function read contacts in
    data file and return list of contacts'''
    with open(db_path, 'rb') as file:
        db_data = pickle.load(file)

    return db_data


def save_db(db_data: list) -> None:
    '''Function save new data to data file'''
    with open(db_path, 'wb') as file:
        pickle.dump(db_data, file)


def view_contacts(db_data_view: list, labels: list, id_contact: str='all') -> None:
    '''Function return contacts to
    console from data file'''

    if id_contact == 'all':
        data = db_data_view
    else:
        data = db_data_view[id_contact - 1:id_contact]
    db_data = read_db()
    print('\n#', end=' ')

    for i in labels:
        print(i[0].ljust(i[1]), sep='\n', end=' ')
    print('')

    for i in data:

        print(db_data.index(i) + 1, end=' ')
        for d in labels:
            print(i.get(d[0], '-')[:d[1] - 2].ljust(d[1]), end=' ')
        print('\n' if i == data[-1] else '')


def action_contact(labels: list, db_data: list, action: str='new', id_contact: int=0) -> None:
    '''Function add new contact to contact
    list, delete contact from contact list, or edit contact
    in db_data and save it to data file'''

    data = dict()
    if action not in 'delete':
        for i in labels:

            if i[0] == 'age':
                try:
                    value = int(
                        input(f'Please Enter {i[0].upper()}: ').strip())
                    data[i[0]] = str(value)
                except:
                    print('*** Bad value, need number ***')
            else:
                value = input(f'Please Enter {i[0].upper()}: ').strip()

                if i[0] == 'name' and len(value) < 3:
                    print('*** Bad name ***')
                    break

                if len(value) < 1:
                    value = '-'

                data[i[0]] = value
    else:
        del db_data[id_contact - 1]

    if action == 'new':
        db_data.append(data)
    elif action == 'edit':
        db_data[id_contact - 1] = data

    save_db(db_data)


def edit_contact(db_data: list, labels: list) -> None:
    '''Function interface to edit user in contact list.'''

    try:

        id_contact = int(input('Pease Enter contact ID: '))

        if id_contact < 1 or id_contact > len(db_data):
            print('Contact not found')
        else:
            data = db_data[id_contact - 1]
            view_contacts(db_data, labels, id_contact=id_contact)
            print('''Please choise action: 

            [1] - Edit contact
            [2] - Delete contact
            ''')
            action = input('Action: ')

            if action == '1':
                action_contact(labels, db_data, action='edit',
                               id_contact=id_contact)
            elif action == '2':
                action_contact(labels, db_data, action='delete',
                               id_contact=id_contact)
            else:
                print(f'"{action}" is not support now')

    except:
        id_contact = 'all'
        print('ID must be the number')


def search_contact(db_data: list, labels) -> None:
    '''Function search key in database'''
    search_key = input('Please enter search key: ')

    search_data = []
    for user_data in db_data:
        for data in user_data:
            if search_key in user_data[data]:
                search_data.append(user_data)
                break
    view_contacts(search_data, labels)


if __name__ == '__main__':
    print(__doc__)
    db_name = input('Please enter DB name: ')
    db_path = check_db(db_name)
    menu()
