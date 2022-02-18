from config import c_id, c_se
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import codecs
import pandas as pd

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(c_id, c_se))


def check_csv(fp: [str] = None, sep: [str] = ","):
    if not fp:
        print("no file path given")
        return
    with codecs.open(fp, 'r', encoding="utf-8") as f:  # open as simple text file
        csv_lines = f.read().splitlines()
    csv_lines_with_errors = []
    header_split_num = len(csv_lines[0].split(sep))
    for line_num in range(len(csv_lines)):
        if len(csv_lines[line_num].split(sep)) != header_split_num:
            csv_lines_with_errors.append((line_num + 1))
    if csv_lines_with_errors:
        for error in csv_lines_with_errors:
            print(f"Line: {error}")
    return csv_lines_with_errors


def get_track_features(this_id):
    meta = sp.track(this_id)
    features = sp.audio_features(this_id)
    # meta
    name = meta["name"].replace(";", ",")
    album = meta["album"]["name"]
    artist = meta["album"]["artists"][0]["name"]
    release_date = meta["album"]["release_date"]
    length = meta["duration_ms"]
    popularity = meta["popularity"]
    # features
    acousticness = features[0]["acousticness"]
    danceability = features[0]["danceability"]
    energy = features[0]["energy"]
    instrumentalness = features[0]["instrumentalness"]
    liveness = features[0]["liveness"]
    loudness = features[0]["loudness"]
    speechiness = features[0]["speechiness"]
    tempo = features[0]["tempo"]
    time_signature = features[0]["time_signature"]
    track = [name, album, artist, release_date, length, popularity, danceability, acousticness, energy,
             instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    return track


def songs_by_artist(this_artist: [str] = None):
    if not this_artist:
        print("no artist provided.")
        return None
    songs = sp.search(q=this_artist, type="track", limit=50, market="GB")
    song_id_lst = []
    for _ in range(len(songs["tracks"]["items"])):
        if songs["tracks"]["items"][_]["name"] != this_artist:
            song_id_lst.append(songs["tracks"]["items"][_]["id"])
    return song_id_lst


def save_track_features_to_csv(this_id: [str] = None, fp: [str] = None):
    if not fp:
        print("no file path given")
        return
    if not this_id:
        print("no id provided.")
        return
    meta = sp.track(this_id)
    features = sp.audio_features(this_id)
    if features == [None]:
        return
    # meta
    name = meta["name"].replace(";", ",")
    album = meta["album"]["name"].replace(";", ",")
    artist = meta["album"]["artists"][0]["name"].replace(";", ",")
    release_date = meta["album"]["release_date"]
    length = meta["duration_ms"]
    popularity = meta["popularity"]
    # features
    acousticness = features[0]["acousticness"]
    danceability = features[0]["danceability"]
    energy = features[0]["energy"]
    instrumentalness = features[0]["instrumentalness"]
    liveness = features[0]["liveness"]
    loudness = features[0]["loudness"]
    speechiness = features[0]["speechiness"]
    valence = features[0]["valence"]
    key = features[0]["key"]
    mode = features[0]["mode"]
    tempo = features[0]["tempo"]
    type_ = features[0]["type"]
    time_signature = features[0]["time_signature"]
    with codecs.open(fp, "a+", encoding="utf-8") as f:
        f.write(f"{this_id};{name};{album};{artist};{release_date};{length};{popularity};{danceability};{acousticness};"
                f"{energy};{instrumentalness};{liveness};{loudness};{speechiness};{valence};{key};{mode};{tempo};"
                f"{type_};{time_signature}\n")


def create_csv(fp: [str] = None):
    # ** use 1000 top streamed artist list **
    # with open("./data/most_streamed_artists.txt", "r") as f:
    #     c = f.readlines()
    # artists = [a.strip("\n") for a in c]

    # ** set another list of artists **
    # artists = ["Massive Attack", "Archive", "Ani DiFranco", "Garbage", "Melano", "Chaos Chaos", "Flyleaf", "Robyn"]

    # ** use artists from the longest playlist on spotify **
    # artists = return_unique_artists_list("./data/artists_list.csv")
    with open("./data/final_cleaned_artist_lst.csv", "r") as f:
        c = f.readlines()
    artists = [a.strip("\n") for a in c[1077:]]
    # first run:
    # Buckcherry(534 / 3836)
    # Built to Spill(535 / 3836)
    # 3rd run from [1077:]

    counter = 0
    for artist in artists:
        counter += 1
        print(f"{artist} ({counter:3d} / {len(artists)}) - songs: ", end="")
        this_artist_songs = songs_by_artist(artist)
        print(len(this_artist_songs))
        if not this_artist_songs:
            print(f"Skipped: {artist}")
            continue
        for index in range(len(this_artist_songs)):
            save_track_features_to_csv(this_artist_songs[index], fp)


if __name__ == "__main__":
    # DO YOU NEED TO RUN THIS? clean_artists_file("./data/all_artists.txt")
    fp_used = "./data/song_db.csv"

    create_csv(fp=fp_used)
    check_csv(fp_used, ";")
