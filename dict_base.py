import re
import sqlite3

#counts = dict()
conn = sqlite3.connect('english_turkish.sqlite')
cur = conn.cursor()

try:
	cur.execute('SELECT English_id FROM Turkish ORDER BY id DESC')
	id=cur.fetchone()[0]
	print(id, 'words in dictionary')
except:
	id=0
	print('no value in db')

cur.close()
while True:
	translate = input('\nenter english word: ')
	if len(translate)<1:
		reply = input('check for changes and rebuild database? "yes/no": ')
		if reply == 'yes':
			#file chooser
			name = input('Enter file name: ')
			if len(name)<1:
				name = 'lugat1.xls'
			try:
				handle = open(name, encoding="utf-8")
				handle2 = open(name, encoding="utf-8")
				print('database rebuilding..')
			except FileNotFoundError:
				print('!!! wrong file name !!!')
				continue
			wordCount=0
			#word counter in file
			for line in handle:
				wordCountNew = re.findall('([0-9]+)\t', line)
				#print(wordCount)
				if len(wordCountNew)>0 and int(wordCountNew[0])>wordCount:
					wordCount=int(wordCountNew[0]) # count the highest number in excel file
					#print(wordCountNew[0])
					#print(int(wordCountNew[0]))	
			print('Source wordCount:', wordCount, ' DB id count:', id)
			if wordCount>id:
				cur=conn.cursor()
				cur.execute('CREATE TABLE IF NOT EXISTS English (id INTEGER PRIMARY KEY, english TEXT UNIQUE)')
				cur.execute('CREATE TABLE IF NOT EXISTS Turkish (id INTEGER PRIMARY KEY, English_id INT UNIQUE, turkce TEXT)')
				conn.commit()
				print('tables created')				#print('wordCount', wordCount, 'id', id)\
				addcount=0
				idCounter = id+1
				for line2 in handle2:	
					#words = line2.split()
					#for word in words:
						#counts[word] = counts.get(word,0) + 1
					#print(idCounter)
					wordCountCheck = re.findall('([0-9]+)\t', line2)
					english = re.findall(f'^{idCounter}\t(.*)\t', line2)
					#print(english)
					turkish = re.findall('\t.*\t(.*)', line2)	
					#print('id', idCounter)
					if len(wordCountCheck)>0:
						wordCountCheck=int(wordCountCheck[0])
						#print('wcc', wordCountCheck)
					if wordCountCheck == idCounter:
						#print('checkpoint')
						addcount = addcount+1
						#if len(english)>0:
						cur.execute('INSERT OR IGNORE INTO English (english) VALUES(?)', (english))
						conn.commit()
						cur.execute('SELECT id FROM English WHERE english=?', english)
						english_id= cur.fetchone()[0]
						cur.execute('INSERT OR IGNORE INTO Turkish (English_id, turkce) Values(?, ?)', (english_id,  turkish[0],))
						conn.commit()
						if addcount % 100 == 0:
							print(english_id, english, 'turkish: ', turkish)
						idCounter = idCounter+1 
				#print('checkpoint')
				conn.commit()
				cur.close()
				id=idCounter-1
		else:
			continue
	elif translate == 'exit':
		break
	else:
		cur = conn.cursor()
		cur.execute('SELECT id FROM English WHERE english=?', (translate, ))
		try: 
			searchId = cur.fetchone()[0] 
			if searchId>0:
				cur.execute('SELECT turkce FROM Turkish WHERE English_id=?', (searchId, ))
				turkce = cur.fetchone()
				result = list()
				for a in turkce:
					a = a.split(',')
					#count = len(a)
					for b in a:
						print('> ' + b.strip())
					cur.close()
				#result = result[0].split()
				#print(result+ '\n')
		except:
			print('!!! unable to find the word !!!')

print('exiting dictionary')
bigcount = None
bigword = None
#for word,count in counts.items():
 #   if bigcount is None or count>bigcount:
  #      bigword = word
   #     bigcount = count