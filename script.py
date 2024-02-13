# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 18:12:40 2023

@author: Ariel
"""

import sys
import pandas
import xml
import datetime

def removeP(s):
    return [s.removeprefix('(').removesuffix(')')]

def getDate(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

def lContains(l, i):
    for li in l:
        if li == i:
            return True
    return False

def lExists(l, p):
    for i in l:
        if p(i):
            return True
    return False

def lFilter(l, p):
    r = []
    for i in l:
        if p(i):
            r.append(i)
    return r

def lFind(l, p):
    for i in l:
        if p(i):
            return i
    return None

def lForAll(l, p):
    for i in l:
        if not p(i):
            return False
    return True

def lMap(l, f):
    r = []
    for i in l:
        r.append(f(i))
    return r

def lTail(l):
    return l[1:]

def remDupl(l):
    d = {}
    for i in l:
        if not i.telephone_number in d:
            d[i.telephone_number] = []
        d[i.telephone_number].append(i)
    
    r = []
    for k in d:
        r.append(max(d[k], key = lambda x: x.created_at))
    return r

def dfList(df):
    r = []
    for p in df.iterrows():
        pr = Person()
        pr.firstname = p[1]['firstname']
        pr.telephone_number = p[1]['telephone_number']
        pr.email = p[1]['email']
        pr.password = p[1]['password']
        pr.role = p[1]['role']
        pr.created_at = p[1]['created_at']
        pr.children = []
        for c in p[1]['children']:
            ch = Child()
            ch.name = c['name']
            ch.age = c['age']
            pr.children.append(ch)
        r.append(pr)
    return r

def processCsv(f):
    # read file
    fl = open(f'data/{f}', 'r')
    fll = fl.readlines()
    
    # close file
    fl.close()
    
    # make DF
    fll = lTail(fll)
    fll = lMap(fll, lambda x: x.removesuffix('\n').split(';'))
    l = []
    for u in fll:
        pr = {}
        pr['firstname'] = u[0]
        pr['telephone_number'] = u[1]
        pr['email'] = u[2]
        pr['password'] = u[3]
        pr['role'] = u[4]
        pr['created_at'] = getDate(u[5])
        pr['children'] = []
        if not u[6] == '':
            cl = u[6].split(',')
            cl = lMap(cl, lambda x: x.split(' '))
            cl = lMap(cl, lambda x: [x[0]] + removeP(x[1]))
            for c in cl:
                ch = {}
                ch['name'] = c[0]
                ch['age'] = int(c[1])
                pr['children'].append(ch)
        l.append(pr)
    df = pandas.DataFrame.from_dict(l)
    
    # load DF to list
    return dfList(df)

def processJson(f):
    # read file
    df = pandas.read_json(f'data/{f}')
    
    # load DF to list
    return dfList(df)

def processXml(f):
    # read file
    root = xml.etree.ElementTree.parse(f'data/{f}').getroot()
    
    # make DF
    l = []
    for u in root:
        pr = {}
        pr['firstname'] = u[0].text
        pr['telephone_number'] = u[1].text
        pr['email'] = u[2].text
        pr['password'] = u[3].text
        pr['role'] = u[4].text
        pr['created_at'] = getDate(u[5].text)
        pr['children'] = []
        for c in u[6]:
            ch = {}
            ch['name'] = c[0].text
            ch['age'] = int(c[1].text)
            pr['children'].append(ch)
        l.append(pr)
    df = pandas.DataFrame.from_dict(l)
    
    # load DF to list
    return dfList(df)

c1 = lambda: len(System.data)

def c2():
    acc = min(System.data, func = lambda x: x.created_at)
    print(f'name: {acc.name}')
    print(f'email_address: {acc.email_address}')
    print(f'created_at: {acc.created_at}')

def c3():
    d = {}
    for p in System.data:
        for c in p.children:
            if c.age in d:
                d[c.age] += 1
            else:
                d[c.age] = 1
    
    l = []
    for k in d:
        l.append((k, d[k]))
    
    l = sorted(l, key = lambda x: x[1])
    for t in l:
        print(f'age: {t[0]}, count: {t[1]}')

def c4():
    c = lMap(System.acc.children, lambda x: [x.name, x.age])
    c = sorted(c, key = lambda x: x[0])
    for ci in c:
        print(f'{ci[0]}, {ci[1]}')

def c5():
    ages = []
    for p in System.data:
        for c in p.children:
            if not c.age in ages:
                ages.append(c.age)
    
    for a in ages:
        sim = lFilter(System.data,
                      lambda x: lExists(x.children, lambda y:
                                        y.age == a))
        stl = []
        for s in sim:
            st = f', {s.telephone_number}: '
            for c in s.children:
                st += f'{c.name}, {c.age}; '
            st = st.removesuffix('; ')
            stl.append((s.firstname, st))
        stl = sorted(stl, key = lambda x: x[0])
        for l in stl:
            print(f'{l[0]}{l[1]}')

class Person:
    pass

class Child:
    pass

class System:
    def init():
        # check command
        cmds = [
            'print-all-accounts',
            'print-oldest-account',
            'group-by-age',
            'print-children',
            'find-similar-children-by-age'
            ]
        if not lContains(cmds, sys.argv[1]):
            raise AttributeError('Invalid Command')
        System.cmd = sys.argv[1]
        
        # try getting login
        if not sys.argv[2] == '--login':
            print('Invalid Login')
            sys.exit(1)
        System.login = sys.argv[3]
        
        # try getting password
        if not sys.argv[4] == '--password':
            print('Invalid Login')
            sys.exit(1)
        System.password = sys.argv[5]
    
    def importData():
        # load files
        csvFiles = ['a/b/users_1.csv', 'a/c/users_2.csv']
        jsonFiles = ['a/users.json']
        xmlFiles = ['users_2.xml', 'a/b/users_1.xml']
        System.data = []
        for f in csvFiles:
            System.data += processCsv(f)
        for f in jsonFiles:
            System.data += processJson(f)
        for f in xmlFiles:
            System.data += processXml(f)
        
        # validate and perhaps edit or reject entries
        # criterion 1 (emails)
        c1_1 = lambda x: x.count('@') == 1
        c1_2 = lambda x: len(x.split('@')[0]) >= 1
        c1_3 = lambda x: len(x.split('@')[1].split('.')[0]) >= 1
        lp = lambda x: x.split('.')[-1]
        c1_4_1 = lambda x: len(lp(x)) in range(1, 5)
        c1_4_2 = lambda x: lp(x).isalnum()
        c1 = lambda x: lForAll(
            [c1_1(x), c1_2(x), c1_3(x), c1_4_1(x), c1_4_2(x)],
            lambda y: y
            )
        System.data = lFilter(
            System.data, lambda x: c1(x.email))
        # criterion 2 (non-empty phone numbers)
        c2 = lambda x: len(x) > 0
        System.data = lFilter(
            System.data, lambda x: c2(x.telephone_number))
        # criterion 3 (no duplicates)
        System.data = remDupl(System.data)
        # criterion 4 (format phone numbers)
        f4_1 = lambda x: x.removeprefix('+48')
        def f4_2(x):
            if len(x) > 9:
                return x.removeprefix('00')
            else:
                return x
        f4_3 = lambda x: x.removeprefix('(48)')
        f4_4 = lambda x: x.replace(' ', '')
        def f4(p, f):
            p.telephone_number = f(p.telephone_number)
            return p
        for f in [f4_1, f4_2, f4_3, f4_4]:
            System.data = lMap(System.data, lambda x: f4(x, f))
    
    def loginF():
        d = System.data
        l = System.login
        p = System.password
        if l.count('@') == 1:
            lt = 0
        else:
            lt = 1
        if lt == 0:
            acc = lFind(d, lambda x:
                        x.email == l and x.password == p)
        else:
            acc = lFind(d, lambda x:
                        x.telephone_number == l
                        and x.password == p)
        if acc == None:
            print('Invalid Login')
            sys.exit(1)
        else:
            System.acc = acc
            System.role = acc.role
    
    def runCmd():
        admCmds = [
            'print-all-accounts',
            'print-oldest-account',
            'group-by-age'
            ]
        cmd = System.cmd
        if System.role == 'user' and lContains(admCmds, cmd):
            raise BaseException('Not Authorized')
        if cmd == 'print-all-accounts':
            c1()
        elif cmd == 'print-oldest-account':
            c2()
        elif cmd == 'group-by-age':
            c3()
        elif cmd == 'print-children':
            c4()
        else:
            c5()

System.init()
System.importData()
System.loginF()
System.runCmd()