import urllib2
import time
import datetime

wxurl="http://api.wunderground.com/weatherstation/WXDailyHistory.asp?ID=KCASANFR941&format=RAW"
wxfile = "C:\\Weather\\zara.html"
response = urllib2.urlopen(wxurl)
html = response.readlines()
response.close()
idx = len(html)-2
parts = html[idx].split(",")
obstime = time.mktime(datetime.datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S").timetuple())
deltatime = time.mktime(datetime.datetime.now().timetuple()) - obstime
temperature = float(parts[1])
humidity = int(parts[8])
temp_f = int(round(temperature,0))

linesout = []
linesout.append('<HTML>')
linesout.append('Temperature: '+str(temp_f)+'<BR/>')
linesout.append('Humidity: '+str(humidity)+'<BR/>')
linesout.append('</HTML>')

if deltatime < 3600:
    f = open(wxfile,'w')
    f.write("\n".join(linesout))
    f.close()
