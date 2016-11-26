Zara Helpers
==
This is a set of scripts that can be used to get more functionality from the freeware version of ZaraRadio
http://www.zarastudio.es/download.php

ZaraRadio is a light-weight Windows application for radio station automation. Zara's strong point as I see them are:

* Low resource consumption, it runs well on modest hardware.
* No relational database server required! Audio content are just sound files.
* Time and Temperature announce support.
* Very flexible event system.
* Straight-forward UI.
* Free (as in beer).

The shortfalls of the freeware version as I see them are:

* Limited playlist generation - you can playback a list in shuffle, but you can easily play the same artist multiple times in a row. You can set the list to play in random, but there is no garauntee that tracks won't repeat back-back or in a short period of time. There is no defineable artist separation or track repeat rules. (Note: the paid version does include these features).
* The automatic weather retrieval for temperature and humidity announcements uses a not free 3rd party utility to download the data from major reporting locations, such as airports.

These scripts let me take advantage of the good stuff while filling in some of the shortfalls of the free ZaraRadio version.

Playlist Generation
==
**dbload.py** - this script reads a Zara playlist file and loads the tracks into a file based SQLite database. I infer some information from the file system layout. Essentially that all the tracks for the format are in directories for each artist under a base directory. 

Like C:\MyRadioStation\Format\Artist\Track_Title.mp3 e.g. C:\AM1700\BigBand\Artie Shaw\Any_Old_Time.mp3

The SQLite database schema is exceedingly simple:

`CREATE TABLE tracks (title text, artist text, lastplay integer, playcount integer, duration integer, fullpath text);`

* lastplay is in seconds since the beginning of the Epoch (1 Jan 1970).
* duration is the track length in milliseconds.
* fullpath is the fully qualified path and file name of the track.
* track title and artist are derived from the fullpath.

The database design could certainly be more sophisticated and efficient, but I opted for simplicity and expedience. The playlist generation script assumes the SQLite file and tracks table have already been created, it will not create it automatically.

**scheduler.py** - this script generates Zara playlist files from the tracks in the SQLite database file. You can set the artist separation time, track repeat limit time, and playlist length (all in seconds) in the code.

The track repeat is actually a title repeat rule so if you have two or more tracks with the same title by different artists (covers & standards) they will not play too close to eachother.

The artist sepration and track repeat intervals could be derived by analyzing track statistics but that's beyond the scope of the this release. Using this code you'll need to figure out the values empirically. Either it will generate a playlist or it will hang, forever trying to meet the rules. Obviously, more tracks and artists is better.

**scanlog.py** - this script (not released yet) will scan the Zara log and update the lastplay and playcount in the SQLite database. This will script will be helpful in generating playlists that maintain artist and track separation with respect to what has actually been played out.

The general workflow is:

1. create the database file and 'tracks' table using the sqlite cmd line utility (http://www.sqlite.org/download.html) 
2. create a playlist in Zara by dragging the tracks or folders from the explorer pane.
3. Save the .lst file from Zara
4. Run the dbload.py script to get the tracks into the database
5. Run the scheduler.py script to create a playlist of any length with artist separation and title/track repeat rules.

I set up a scheduled task in windows to do step 5 once a day. An event in Zara loads the generated playlist file.

When I need to add music to the database I repeat steps 2 through 4 for the new music only.

Weather Help
==
**getweather.py** - this script scrapes temperature and humidity from WeatherUnderground personal weather station (PWS) report pages. My use of Zara is with a Part 15 AM radio station, which has coverage of about a city block. It doesn't make sense to report the hourly airport temperature or even the temperature downtown, I need the realtime temperature for my neighborhood.

The script writes an html file that can be read by Zara to keep the temperature and humidity updated in the application. I have a scheduled windows event that runs this script to update the temperature every 10 minutes.

Support
==
This code is released into the Public Domain with The Unlicense (read it). The software is absolutely and completely unsupported. Use at your own risk, your mileage may very, etc, etc. If you decide to use these scripts, you are responsible for getting it to work for you.

I suggest studying the code to understand how it works (it's not too complex) and thus how you can customize for your own use.

Good Luck and Happy Broadcasting.
