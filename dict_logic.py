import sqlite3
import re

def conDB(name):
    con=sqlite3.connect(name)
    return con

def initDB(name):
    cur=conDB(name).cursor()
    return cur

def search(word, dbname):
    cur = initDB(dbname)
    if len(word) < 1:
        yield('')
    else:
        try:
            cur.execute('SELECT id FROM English WHERE english=?', (word,))
            searchId = cur.fetchone()[0]
            if searchId > 0:
                cur.execute('SELECT turkce FROM Turkish WHERE English_id=?', (searchId,))
                turkce = cur.fetchone()
                result = list()
                for a in turkce:
                    a = a.split(',')
                    # count = len(a)
                    for b in a:
                        yield('> ' + b.strip())
                # result = result[0].split()
                # print(result+ '\n')
        except:
            yield('!!! unable to find the word in database !!!')

def add(english,turkish, dbname):
    con = conDB(dbname)
    cur = con.cursor()
    cur.execute(
        'INSERT OR IGNORE INTO English (english) VALUES(?)', (english,))
    con.commit()
    cur.execute('SELECT id FROM English WHERE english=?', (english,))
    english_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO Turkish (English_id, turkce) Values(?, ?)',
                (english_id, turkish))
    con.commit()
    cur.close()

def build(dbname, filename, count):
    con = conDB(dbname)
    cur = con.cursor()
    if len(filename) < 1:
        filename = 'lugat1.xls'
    try:
        handle = open(filename, encoding="utf-8")
        handle2 = open(filename, encoding="utf-8")
        print('database rebuilding..')
    except FileNotFoundError:
        print('!!! wrong file name !!!')
    wordCount = 0
    # word counter in file
    for line in handle:
        wordCountNew = re.findall('([0-9]+)\t', line)
        # print(wordCount)
        if len(wordCountNew) > 0 and int(wordCountNew[0]) > wordCount:
            wordCount = int(wordCountNew[0])  # count the highest number in excel file
    global id  # declare this to prevent error in the upcoming line
    print('Number of words in user file:', wordCount, 'vs in database:', count)
    if wordCount > count:
        cur.execute(
            'CREATE TABLE IF NOT EXISTS English (id INTEGER PRIMARY KEY, english TEXT UNIQUE)')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS Turkish (id INTEGER PRIMARY KEY, English_id INT UNIQUE, turkce TEXT)')
        conn.commit()
        print('tables created')  # print('wordCount', wordCount, 'id', id)\
        addcount = 0
        idCounter = id + 1
        for line2 in handle2:
            wordCountCheck = re.findall('([0-9]+)\t', line2)
            english = re.findall(f'^{idCounter}\t(.*)\t', line2)
            # print(english)
            turkish = re.findall('\t.*\t(.*)', line2)
            # print('id', idCounter)
            if len(wordCountCheck) > 0:
                wordCountCheck = int(wordCountCheck[0])
                # print('wcc', wordCountCheck)
            if wordCountCheck == idCounter:
                # print('checkpoint')
                addcount = addcount + 1
                # if len(english)>0:
                cur.execute(
                    'INSERT OR IGNORE INTO English (english) VALUES(?)', (english))
                dict_logic.conDB(dbname).commit()
                cur.execute('SELECT id FROM English WHERE english=?', english)
                english_id = cur.fetchone()[0]
                cur.execute('INSERT OR IGNORE INTO Turkish (English_id, turkce) Values(?, ?)',
                            (english_id, turkish[0],))
                dict_logic.conDB(dbname).commit()
                if addcount % 100 == 0:
                    print(english_id, english, 'turkish: ', turkish)
                idCounter = idCounter + 1
        # print('checkpoint')
        dict_logic.conDB(dbname).commit()
        id = idCounter - 1
    else:
        print('Database build up aborted due to less number of words.')
    cur.close()