import argparse
from pymongo import MongoClient
import pickle


def get_documents(path):
    with open(path, 'rb') as file:
        data = pickle.load(file)
    documents = [{key: values} for key, values in data.items()]
    return documents


def get_documents_2(path):
    with open(path, 'rb') as file:
        data = pickle.load(file)
    return list(data)


def setup(ip, port):
    client = MongoClient(host=ip, port=port)

    book_path = './app/database/books_database.pkl'
    book_documents = get_documents(book_path)
    book_collection = client['final_project']['book']
    _ = book_collection.insert_many(book_documents)

    song_path = './app/database/songs_database.pkl'
    song_documents = get_documents(song_path)
    song_collection = client['final_project']['song']
    _ = song_collection.insert_many(song_documents)

    movie_path = './app/database/movies_database.pkl'
    movie_documents = get_documents(movie_path)
    movie_collection = client['final_project']['movie']
    _ = movie_collection.insert_many(movie_documents)

    play_path = './app/database/plays_database.pkl'
    play_documents = get_documents(play_path)
    play_collection = client['final_project']['play']
    _ = play_collection.insert_many(play_documents)

    selection_path = './app/database/selection_history_database.pkl'
    selection_documents = get_documents_2(selection_path)
    selection_collection = client['final_project']['selection_history']
    _ = selection_collection.insert_many(selection_documents)

    diary_path = './app/database/diary_history_database.pkl'
    diary_documents = get_documents_2(diary_path)
    diary_collection = client['final_project']['diary_history']
    _ = diary_collection.insert_many(diary_documents)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='local', help='MongoDB Server IP')
    parser.add_argument('--port', type=int, default=27017, help='MongoDB port number')

    setup(parser.ip, parser.port)




