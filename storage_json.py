from istorage import IStorage
import json
import requests
import random


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def load_movie_data(self):
        with open(self.file_path) as file:
            return json.load(file)

    def save_movie_data(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=2)

    def list_movies(self):
        movies = self.load_movie_data()
        print(f"\n{len(movies)} movies in total")
        if not movies:
            print("\nNo movies in your database")
        else:
            for movie, data in movies.items():
                print(f"{movie}: {data['rating']}")

    def add_movie(self):
        title = input("Enter Movie Title: ")
        response = requests.get(f"http://www.omdbapi.com/?apikey=f465fdc9&t={title}")
        if response.status_code == 200:
            movie_data = response.json()
            if movie_data["Response"] == "True":
                year = movie_data["Year"]
                rating = movie_data["imdbRating"]
                poster_url = movie_data["Poster"]

                data = self.load_movie_data()
                data[title] = {"year": year, "rating": rating, "poster": poster_url}
                self.save_movie_data(data)
                print(f"Movie '{title}' successfully added.")
            else:
                print(f"Movie '{title}' not found in the OMDb database.")
        else:
            print(f" We got status code {response.status_code}")

    def delete_movie(self):
        title = input("Enter Movie title: ")
        data = self.load_movie_data()
        if title in data:
            del data[title]
            print(f"{title} successfully deleted!")
            self.save_movie_data(data)
        else:
            print(f"Movie {title} not found!")

    def update_movie(self):
        title = input("Enter Movie title: ")
        data = self.load_movie_data()
        if title in data:
            rating = input("Enter new rating 1-10: ")
            data[title]["rating"] = rating
            print(f"Movie '{title}' rating updated to {rating}!")
            self.save_movie_data(data)
        else:
            print(f"Movie '{title}' not found..")

    def random_movie(self):
        movies = self.load_movie_data()
        random_movie = random.choice(list(movies.keys()))
        random_rating = movies[random_movie]["rating"]

        print(f"\nYour random movie: {random_movie} ({float(random_rating):.1f})")
        print()
