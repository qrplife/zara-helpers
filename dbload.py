import sqlite3

listFile = "/home/matt/BigBandImport.lst"
db = "tracks_bigband.sqlite3"

playcount=0
lastplay=0

try:
	f = open(listFile,'r')
	conn = sqlite3.connect(db)
	cur = conn.cursor()
	trackCount = int(f.readline()[:-1])
    # CREATE TABLE tracks (title text, artist text, lastplay datetime, playcount integer, duration integer, fullpath text);
	sql = "INSERT INTO tracks ( title, artist, lastplay, playcount, duration, fullpath ) VALUES ( ?, ?, ?, ?, ?, ?)"
	
	for i in range(trackCount):
		line = f.readline()[:-2]
		lineParts = line.split('\t')
		duration = lineParts[0]
		fullpath = lineParts[1].decode('cp1252')
		fileparts = fullpath.split("\\")
		artist =  fileparts[3]
		title = fileparts[4][:-4]		
		parameters = ( title, artist, lastplay, playcount, int(duration), fullpath )
		#print parameters
		cur.execute(sql,parameters)	

	conn.commit()
finally:
	conn.close()
	f.close()

		


