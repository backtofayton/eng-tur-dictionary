import cmd
import dict_logic

# open database and get the id of the last row to count the words

dbname='english_turkish.sqlite'
cur= dict_logic.initDB(dbname)

try:
    cur.execute('SELECT English_id FROM Turkish ORDER BY id DESC')
    id = cur.fetchone()[0]
    print()
    print(id, 'words in dictionary')
except:
    id = 0
    print('no value in db')

cur.close()

class en_tr(cmd.Cmd):
    intro = '''
Enter a command: "start", "add", "build" or "quit". 
Type "help" for help.
    '''
    prompt = '(translator) > '

    def do_add(self, arg):
        self.en = input('Enter the English word that you want to add: ')
        self.tr = input('Enter the Turkish translation: ')
        self.ask = input(
            'Do you want to add this translation to database? "yes/no" > {}: {} > '.format(self.en, self.tr))
        if (self.ask.lower() == 'yes') or (self.ask.lower() == 'y'):
            dict_logic.add(self.en, self.tr, dbname)
        else:
            return

    def do_start(self, arg):
        self.exitdict = False
        while True:
            if self.exitdict: break
            translate=input('\nEnter an English word > ')
            ## or if (len(translate)<1: break
            result = dict_logic.search(translate, dbname)
            for i in result:
                if (i==''): self.exitdict=True
                print(i)
            cur.close()

    def do_build(self, arg):
        self.filename = input('Enter database file name: ')
        dict_logic.build(dbname, self.filename, id)

    def do_quit(self, arg):
        cur.close()
        print('\nGoodbye..\n')
        raise SystemExit

    def do_help(self, arg):
        print('''
----- English to Turkish Dictionary -----

1) Type 'start' to start using dictionary.
    - Press 'enter' to return to the main menu while using dictionary.

2) Type 'add' to add new word to database. 

3) Type 'build' to build database from scratch or add words in bulk.
    - If no filename is entered 'lugat1.xls' is chosen as default.

4) Type 'quit' to quit application.
''')
        return

def main():
    translator = en_tr().cmdloop()

if __name__ == '__main__':
    main()
