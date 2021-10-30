import re
import requests
from bs4 import BeautifulSoup


file = "clean.txt"
f = open(file, "r")
lines = f.readlines()

# file = "christianese.txt"
# f = open(file, "r")
# linesC = f.readlines()

# Enables web scraping and provides base urls
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
baseURL = "http://azlyrics.com/lyrics/"
baseBackup = "http://genius.com/"

# Doesn't look like this variable ever does anything
switch = ""

while True:

    # Take user inputs for artist and song
    artist = input("Enter artist: ")
    song = input("Enter song: ")

    #idk what this is but it's old
    """
    for a in range(len(artist)):
        if artist[a].isalnum() == False or artist[a] != " ":
            artist = artist.replace()

    for s in range(len(song)):
        if song[s].isalnum() == False or song[s] != " ":
            song[s] = ""
    """

    # Santizing the inputs, no obvious better way to handle atm
    artist = artist.replace(",", "")
    artist = artist.replace("'", "")
    artist = artist.replace(".", "")
    artist = artist.replace("?", "")
    artist = artist.replace("!", "")
    artist = artist.replace(")", "")
    artist = artist.replace("(", "")

    song = song.replace(",", "")
    song = song.replace("'", "")
    song = song.replace(".", "")
    song = song.replace("?", "")
    song = song.replace("!", "")
    song = song.replace(")", "")
    song = song.replace("(", "")

    artist = artist.lower()
    song = song.lower()
    aritst = artist.strip()
    song = song.strip()

    # Adding seperately tracked backups for Genius
    backupArtist = artist
    backupSong = song

    # Removing "The" from artist names for azlyrics
    if artist[0] == "t" and artist[1] == "h" and artist[2] == "e" and artist[3] == " ":
        artist = artist[4:]

    # Replaces spaces with dashes for urls
    artist = artist.replace(" ", "")
    backupArtist = backupArtist.replace(" ", "-")
    song = song.replace(" ", "")
    backupSong = backupSong.replace(" ", "-")

    # The Cardi-B exception
    if artist == "cardib":
        artist = "cardi-b"

    # Concatenating final urls for scraping
    fullURL = baseURL + artist + '/' + song + ".html"
    backupURL = baseBackup + backupArtist + "-" + backupSong + "-lyrics"
    
    #<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->

    # connection checkers
    azcon = True
    gencon = True

    try:
        response = requests.get(fullURL, headers=headers)
    except:
        azcon += False
    try:
        backupResponse = requests.get(backupURL, headers=headers)
    except:
        gencon += False

    # Condition for if both connections fail
    if azcon == False and gencon == False:
        print("The websites could not be reached. Please wait and try again or check your network connection.")
        break
        

    
    # Azlyrics scraping and parsing logic
    if azcon == 0:
        try:
            # Blue will become the full lyrics
            blue = []
            blue = response.text
            blue = BeautifulSoup(blue, 'html.parser')
            blue = blue.get_text()
            blue = blue.split("Search", 1)[1]
            blue = blue.split("if  ( /Android|webOS", 1)[0]
            blue = blue.split("lyrics", 1)[1]
            blue = blue.split("Submit", 1)[0]

            songNotFound = blue.split('.')
            
            
            if songNotFound[0] == " where stars of all genres and ages shine":
                continue
            else:
                blue = blue.strip()
                print("\n" + blue + "\n")
                lyrics = blue.split(" ")
                switch = "az"
                
        except:
            print("Lyrics not found. Check spelling and try agian.\n")
            continue
    
    # Genius scraping and parsing logic
    elif gencon == 0:   
        try:
            gen = []
            gen = backupResponse.text
            gen = BeautifulSoup(gen, 'html.parser')
            gen = gen.get_text()
            gen = gen.split('{"@context', 1)[1]
            gen = gen.split("Lyrics", 1)[1]
            gen = gen.split("More on Genius", 1)[0]

            gen = gen.strip()
            print("\n" + gen + "\n")
            lyrics = gen.split(" ")

            switch = "gen"
            
        except:
            print("Lyrics not found. Check spelling and try agian.\n")
            continue

    
    # Set counters for explicit language
    hits = 0
    totalHits = 0
    # slaps = 0
    # totalSlaps = 0

    # Strips lyrics of all non a-z characters, lyric is just one word on
    # any given pass, and is checked against the full list of curses
 
    # Sanitizing word-by-word through lyrics and checking against explicit language file
    for x in range(len(lyrics)):
        lyric = lyrics[x]
        lyric = lyric.lower()
        lyric = lyric.strip("\n")
        lyric = lyric.replace(",", "")
        lyric = lyric.replace("'", "")
        lyric = lyric.replace(".", "")
        lyric = lyric.replace("?", "")
        lyric = lyric.replace("!", "")
        lyric = lyric.replace(")", "")
        lyric = lyric.replace("(", "")
        lyric = lyric.replace("\"", "")
        #print(lyric)


        # The "lines" variable is the entire contents of the explicit language file, this checks line-by-line (word-by-word) every word in that database against every word in the lyrics using nested for loops... this can't be the most efficient way, right?
        for i in range(len(lines)):
            curse = lines[i]
            curse = curse.strip("\n")
     
            if curse in lyric:
                hits += 1

                if hits == 1:
                    viewLanguage = input("\n\nPossible explicit language. Would you like to view it?  ")
                    viewLanguage = viewLanguage.lower()
                    
                # Code in case of new lines connected to explicits, prints bad words
                if viewLanguage == "yes" or viewLanguage == "y" or viewLanguage == "yeah" or viewLanguage == "ya" or viewLanguage == "yep" or viewLanguage == "affirmative":  
   
                    tempL = lyric.split("\n")
                    totalHits += 1
                    
                    if curse in tempL[0]:
                        print(tempL[0])
                        
                    elif curse in tempL[1]:
                        print(tempL[1])

                    elif curse in tempL[2]:
                        print(tempL[2])


        # Christian secition
        # for k in range(len(linesC)):
        #     fresh = linesC[k]
        #     fresh = fresh.strip("\n")     

        #     if fresh in lyric:
        #         slaps += 1
        #         #print(fresh)
        #         if slaps == 1:
        #             viewLanguage = input("\nPossible Christian Terminology:")
                    


        #         tempL = lyric.split("\n")
        #         totalSlaps += 1
                
        #         if fresh in tempL[0]:
        #             print(tempL[0])
                    
        #         elif fresh in tempL[1]:
        #             print(tempL[1])

        #         elif fresh in tempL[2]:
        #             print(tempL[2])


    # Log totals for user
    if totalHits > 0:            
        print("\nTotal Explicit Words:", totalHits)
    elif totalHits > hits:
        print("\nTotal Explicit Words:", hits)
    else:
        print("This song is clean.")

    # Christian words check
    # if slaps > 0:
    #     print("\nTotal Christian Words:", slaps)
    # else:
    #     print("\nThis song has no Christian terminology.")

    # Check if user wants to continue
    continuation = input("\nWould you like to check another song? ").lower()
    
    if continuation == "yes" or continuation == "y" or continuation == "yeah" or continuation == "yep":
        print("\n")
        continue
    else:
        break

print("\nThank you")
