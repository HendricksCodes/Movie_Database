import json
import requests


def load_movie_data():
    with open("movie_database.json") as file:
        return json.load(file)


def save_movie_data(data):
    with open("movie_database.json", "w") as file:
        json.dump(data, file, indent=2)


def list_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      ...
    }
    """
    return load_movie_data()


def add_movie(title):
    response = requests.get(f"http://www.omdbapi.com/?apikey=f465fdc9&t={title}")
    if response.status_code == 200:
        movie_data = response.json()
        if movie_data["Response"] == "True":
            year = movie_data["Year"]
            rating = movie_data["imdbRating"]
            poster_url = movie_data["Poster"]

            data = load_movie_data()
            data[title] = {"year": year, "rating": rating, "poster": poster_url}
            save_movie_data(data)
            print(f"Movie '{title}' successfully added.")
        else:
            print(f"Movie '{title}' not found in the OMDb database.")
    else:
        print(f" We got status code {response.status_code}")


def delete_movie(title):
    """
    Deletes a movie from the movies' database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    data = load_movie_data()
    if title in data:
        del data[title]
        save_movie_data(data)


def update_movie(title, rating):
    """
    Updates a movie from the movies' database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    data = load_movie_data()
    if title in data:
        data[title]["rating"] = rating
        save_movie_data(data)
