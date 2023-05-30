from istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        pass

    def list_movies(self):
        pass

    def add_movie(self, title, year, rating, poster):
        pass

    def delete_movie(self, title):
        pass

    def update_movie(self, title, notes):
        pass