import sqlite3
import time
import random

# artist separation in seconds ( don't play the same artist more often than this)
artistSeparation = 20 * 60

# title separation in seconds (don't play a given title more often than this. Make sure covers have the same title as original)
titleSeparation = 6 * 60 * 60

# sheduler run time (when is this code running? used to factor track and artist separation with lastplay time)
schedulerRunTime = time.time() # seconds since the Epoch

# playlist desired length in seconds
playlistDesiredLength = 60 * 60 * 16

# playlist scheduled length in seconds
playlistLength = 0

class Track:
    def __init__(self):
        self.title = ""
        self.artist = ""
        self.lastplay = 0
        self.playcount = 0
        self.duration = 0
        self.fullpath = ""
        
def timediff(timeA,timeB):
    return abs(timeA - timeB)

#read all tracks
conn = sqlite3.connect("C:\\MyRadioStation\\tracks.sqlite3")
cur = conn.cursor()
sql = "SELECT * FROM tracks"
cur.execute(sql)
tracks = cur.fetchall()
conn.close()

# gather last play data into dictionaries
artistLastPlayOrSchedule = {}
titleLastPlayOrSchedule = {}
for track in tracks:
    title = track[0]
    artist = track[1]
    lastPlay = track[2]
    
    if title in titleLastPlayOrSchedule:
        if titleLastPlayOrSchedule[title] < lastPlay:
            titleLastPlayOrSchedule[title] = lastPlay
    else:
        titleLastPlayOrSchedule[title] = lastPlay
    
    if artist in artistLastPlayOrSchedule:
        if artistLastPlayOrSchedule[artist] < lastPlay:
            artistLastPlayOrSchedule[artist] = lastPlay
    else:
        artistLastPlayOrSchedule[artist] = lastPlay

playlist = []

while playlistLength < playlistDesiredLength:
    # note where we are in the current schedule
    scheduleNow = int(schedulerRunTime) + playlistLength
    
    # pick a song at random
    track = random.choice(tracks)
    t = Track()
    t.title = track[0]
    t.artist = track[1]
    t.lastplay = track[2]
    t.playcount = track[3]
    t.duration = track[4]
    t.fullpath = track[5]
    
    #test artist separation    
    if timediff(scheduleNow,artistLastPlayOrSchedule[t.artist]) < artistSeparation:
        continue

    #test title separation
    if timediff(scheduleNow,titleLastPlayOrSchedule[t.title]) < titleSeparation:
        continue

    # this track has passed all the disqualifying tests
    playlist.append(t)
    playlistLength += int(t.duration / 1000)
    artistLastPlayOrSchedule[t.artist] = scheduleNow
    titleLastPlayOrSchedule[t.title] = scheduleNow
    

#write playlist file
playlistFile = "C:\\MyRadioStation\\Playlist.lst"
f = open(playlistFile,'w')
f.write(str(len(playlist))+"\n")
for t in playlist:
    f.write("{}\t{}\n".format(t.duration,t.fullpath.encode('cp1252')))
f.close()


