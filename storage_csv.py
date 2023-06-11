import csv
from abc import ABC
from istorage import IStorage


class StorageCsv(IStorage, ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        movies = {}
        with open(self.file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row["title"]
                rating = row["rating"]
                year = row["year"]
                movies[title] = {"rating": rating, "year": year}
        return movies

    def add_movie(self, title, year, rating, poster):
        with open(self.file_path, "a") as file:
            writer = csv.writer(file)
            writer.writerow([title, rating, year])

    def delete_movie(self, title):
        rows = []
        with open(self.file_path, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != title:
                    rows.append(row)
        with open(self.file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def update_movie(self, title, rating):
        rows = []
        with open(self.file_path, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == title:
                    row[1] = rating
                rows.append(row)
        with open(self.file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
