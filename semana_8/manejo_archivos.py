with open ("songs.txt", "r") as entry_archive:
    songs = entry_archive.readlines() 

songs = [song.strip() for song in songs]
songs_sorted = sorted(songs)


with open ("songs_sorted.txt", "w") as output_archive:
    for song in songs_sorted:
        output_archive.write(song + "\n")

print ("The songs have been sorted and saved as 'songs_sorted.txt'.")