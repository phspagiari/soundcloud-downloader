##
# SOUNDCLOUD DOWNLOADER CLI
# @Author: Pedro H. Spagiari
# @Email: phspagiari@gmail.com
#
# Only to study purposes. 
# I do not agree with the use for piracy and I am not liable for the use of the script to this end.
##

##
# To use Just put the SoundCloud URL as first argument:
# $: python soundcloud-downloader.py http://soundcloud.com/user/music-123
##

import re
import sys
import json
import urllib2

from BeautifulSoup import BeautifulSoup


#### GET URL FROM SYSARGV ####
if len(sys.argv) == 2:
    if re.match("http(s|)://(www.|)soundcloud.com/(.*)", sys.argv[1]):        
        url_soundcloud = sys.argv[1] 
else:
    raise ValueError("Plase put a soundcloud url as first arg")


### ACTUALLY STRING TO GET THE STREAM LINK ###
matchstring = "streamUrl"

### BEGIN MANIPULATION OF HTML AND CONVERT IT TO A DICTIONARY ###
request = urllib2.urlopen(url_soundcloud)
html_page = request.read()
soup = BeautifulSoup(html_page)

# Find in html the json with stream data #
soup_search = soup.html.findAll(text=re.compile(matchstring))
# The first json is always the main stream so #
soup_search = soup_search[0]

# Try to convert the json string into a real json 
possible_json_acceptable = soup_search.strip('\nwindow.SC.bufferTracks.push()').strip(');').replace("'", "\"")
music_data = json.loads(possible_json_acceptable)

music_name = music_data['title']
base_url = 'http://media.soundcloud.com/stream'
token = music_data['token']
download_uri = music_data['uid']

stream_url = "%s/%s?stream_token=%s" % (base_url, download_uri, token)
file_name = "%s.mp3" % (music_name)
file_name = file_name.replace("/", "-")

### DOWNLOAD THE FILE ###
try:
    download_request = urllib2.urlopen(stream_url)
    file_raw = open(file_name, 'wb')
    metadata = download_request.info()
    file_size = int(metadata.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = download_request.read(block_sz)
        if not buffer:
            break
    
        file_size_dl += len(buffer)
        file_raw.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    file_raw.close()
except urllib2.URLError, e:
    print "Download url is invalid", e
