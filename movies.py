import movie_storage
import random
import colorama
from thefuzz import fuzz
from colorama import Fore

# initialize colorama
colorama.init()

# set color constants
ERROR_COLOR = Fore.RED
MENU_COLOR = Fore.WHITE
USER_INPUT = Fore.YELLOW
COMP_RESPONSE = Fore.GREEN


def main():
    """This function generates the command menu and initiates each function based on the input received from the user"""
    print(MENU_COLOR + " *** My Movie Collection *** ")
    while True:
        print(COMP_RESPONSE + "\nWhat would you like to do?:\n")
        print(MENU_COLOR + "0 - Exit Database")
        print(MENU_COLOR + "1 - List Movie_Night")
        print(MENU_COLOR + "2 - Add Movie")
        print(MENU_COLOR + "3 - Delete Movie")
        print(MENU_COLOR + "4 - Update Movie")
        print(MENU_COLOR + "5 - Stats")
        print(MENU_COLOR + "6 - Random Movie")
        print(MENU_COLOR + "7 - Search Movie")
        print(MENU_COLOR + "8 - Movie_Night Sorted By Rating")
        print(MENU_COLOR + '9 - Generate Website')
        choice = input("Enter choice (1-8): " + USER_INPUT)
        if choice == "0":
            exit_database()
        elif choice == "1":
            movie_list()
            input(COMP_RESPONSE + "\nPress Enter to Continue")
        elif choice == "2":
            add_movie()
            input(COMP_RESPONSE + "\nPress Enter to Continue")
        elif choice == "3":
            delete_movie()
            input(COMP_RESPONSE + "\nPress Enter to Continue")
        elif choice == "4":
            update_movie()
            input(COMP_RESPONSE + "\nPress Enter to Continue")
        elif choice == "5":
            movie_stats()
            input(COMP_RESPONSE + "\nPress Enter to Continue")
        elif choice == "6":
            random_movie()
            input(COMP_RESPONSE + "\nPress Enter to Continue")
        elif choice == "7":
            search_movie()
            input(COMP_RESPONSE + "\nPress Enter to Continue")
        elif choice == "8":
            sorted_by_rating()
            input(COMP_RESPONSE + "\nPress Enter to Continue")
        elif choice == "9":
            generate_website()
            input(COMP_RESPONSE + "\nPress Enter to Continue")
        else:
            print(ERROR_COLOR + "Invalid command.")
        print()


def exit_database():
    print(COMP_RESPONSE + "\nHave a nice day!")
    quit()


def movie_list():
    """Displays the list of movies stored in the movie database"""
    movies = movie_storage.list_movies()
    print(COMP_RESPONSE + f"\n{len(movies)} movies in total")
    print("----------------")
    if not movies:
        print("\nNo movies in your database")
    else:
        for movie, data in movies.items():
            print(f"{movie}: {data['rating']}")


def add_movie():
    """
        Adds a movie to the movies database by taking the movie title from the user.
        The function calls the `add_movie` function from `movie_storage` module to fetch
        movie details from the OMDb API and save them in the database.
        """
    title = input("Enter the movie title: ")
    movie_storage.add_movie(title)


def delete_movie():
    # Get the data from the JSON file
    movies = movie_storage.list_movies()

    title = input("Enter the name of the movie to delete: ")
    movie_match = [movie for movie in movies.keys() if fuzz.ratio(title.lower(), movie.lower()) >= 80]

    if len(movie_match) == 0:
        print(ERROR_COLOR + f"The movie '{title}' was not found in the database")
    elif len(movie_match) == 1:
        movie_to_delete = movie_match[0]
        movie_storage.delete_movie(movie_to_delete)
        print(f"'{movie_to_delete}' has been successfully deleted!")
    else:
        print(ERROR_COLOR + f"Multiple movies found with similar names. Be more specific")
    print()


def update_movie():
    # Get the data from the JSON file
    movies = movie_storage.list_movies()

    title = input(USER_INPUT + "Enter the name of the movie to update: ")
    if title in movies:
        rating = float(input(USER_INPUT + "Enter the new rating of the movie (out of 10): "))
        movies[title]["rating"] = rating
        movie_storage.update_movie(title, rating)
        print(f"{title} has been updated with a new rating of {rating}/10.")
    else:
        print(ERROR_COLOR + f"{title} was not found in the movie list.")
    print()


def movie_stats():
    # Get the data from the JSON file
    movies = movie_storage.list_movies()

    if not movies:
        print(ERROR_COLOR + "No movies in the database.")
        return

    # Extract ratings from movies and convert them to floats
    ratings = [float(data["rating"]) for data in movies.values()]

    # Calculate average rating
    avg_rating = sum(ratings) / len(ratings)
    print(f"Average rating: {avg_rating:.2f}")

    # Calculate the median rating
    sorted_ratings = sorted(ratings)
    median_index = len(sorted_ratings) // 2
    if len(sorted_ratings) % 2 == 0:
        median_rating = sum(sorted_ratings[median_index - 1:median_index + 1]) / 2
    else:
        median_rating = sorted_ratings[median_index]
    print(f"Median rating: {median_rating:.2f}")

    # Find the best and worst movies
    max_rating = max(ratings)
    min_rating = min(ratings)
    best_movies = [movie for movie, data in movies.items() if float(data["rating"]) == max_rating]
    worst_movies = [movie for movie, data in movies.items() if float(data["rating"]) == min_rating]
    print(f"Best movie(s): {', '.join(best_movies)}")
    print(f"Worst movie(s): {', '.join(worst_movies)}")
    print()


def random_movie():
    # Get the data from the JSON file
    movies = movie_storage.list_movies()
    random_movie = random.choice(list(movies.keys()))
    random_rating = movies[random_movie]["rating"]

    print(f"\nYour random movie: {random_movie} ({float(random_rating):.1f})")
    print()


def search_movie():
    # Get the data from the JSON file
    movies = movie_storage.list_movies()

    movie_search = input(USER_INPUT + "Enter part of movie name: ")
    movie_match = [movie for movie in movies.keys() if fuzz.ratio(movie_search.lower(), movie.lower()) >= 70]

    if len(movie_match) > 0:
        for movie in movie_match:
            print(f"{movie}: {float(movies[movie]['rating']):.1f}")
    else:
        print(ERROR_COLOR + f"The movie '{movie_search}' does not exist. Did you mean:")
        movie_suggestions = [movie for movie in movies.keys() if fuzz.ratio(movie_search.lower(), movie.lower()) >= 50]
        if len(movie_suggestions) > 0:
            for movie in movie_suggestions:
                print(movie)
    print()


def sorted_by_rating():
    # Get the data from the JSON file
    movies = movie_storage.list_movies()

    if not movies:
        print(ERROR_COLOR + "No movies in the database.")
        return

    # Sort movies by rating
    sorted_movies = sorted(movies.items(), key=lambda x: float(x[1]['rating']), reverse=True)

    # Print sorted movies
    print()
    for movie, data in sorted_movies:
        print(f"{movie}: {data['rating']}")


def generate_website():
    movies = movie_storage.list_movies()
    movie_grid = ""

    for title, info in movies.items():
        movie_title = title
        movie_year = info["year"]
        movie_poster = info.get("poster", "")

        movie_item = f"""
        <li class="movie">
            <img src="{movie_poster}" class="movie-poster" alt="{movie_title} Poster">
            <div class="movie-details">
                <p class="movie-title">{movie_title}</p>
                <p class="movie-year">{movie_year}</p>
            </div>
        </li>
        """
        movie_grid += movie_item

    with open("index.html", "w") as file:
        with open("index_template.html", "r") as template_file:
            template = template_file.read()
            template = template.replace("__TEMPLATE_TITLE__", "My Movie Collection")
            template = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
            file.write(template)

    print("Website was generated successfully.")


if __name__ == "__main__":
    main()
