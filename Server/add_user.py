#!/usr/bin/python3 -B

import os

os.chdir('/home/ftps/Prog/Python/Server/Data')

with open('User.txt', 'a') as f:
    user = input('Input new user: ')
    password = input('Input user password: ')
    access_lvl = input('Input user access level (1 to 3): ')
    if access_lvl != '1' and access_lvl != '2' and access_lvl != '3':
        access_lvl = '3'

    f.write(user + '\t' + password + '\t' + access_lvl)
