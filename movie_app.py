from storage_json import StorageJson
import colorama
from colorama import Fore

# initialize colorama
colorama.init()

# set color constants
ERROR_COLOR = Fore.RED
MENU_COLOR = Fore.WHITE
USER_INPUT = Fore.YELLOW
COMP_RESPONSE = Fore.GREEN


class MovieApp:
    def __init__(self, storage: StorageJson):
        self._storage = storage

    def _command_list_movies(self):
        movies = self._storage.list_movies()
        return movies

    def _command_movie_stats(self):
        movies = self._storage.load_movie_data()
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

    def _generate_website(self):
        movies = self._storage.load_movie_data()
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

    def run(self):
        movies = self._command_list_movies()
        print(MENU_COLOR + " *** My Movie Collection *** ")
        while True:
            print(COMP_RESPONSE + "\nWhat would you like to do?:\n")
            print(MENU_COLOR + "0 - Exit Database")
            print(MENU_COLOR + "1 - List Movies")
            print(MENU_COLOR + "2 - Add Movie")
            print(MENU_COLOR + "3 - Delete Movie")
            print(MENU_COLOR + "4 - Update Movie")
            print(MENU_COLOR + "5 - Stats")
            print(MENU_COLOR + "6 - Random Movie")
            print(MENU_COLOR + '7 - Generate Website')
            choice = input("Enter choice (1-8): " + USER_INPUT)
            if choice == "0":
                print("Goodbye!")
                exit()
            elif choice == "1":
                self._command_list_movies()
                input(COMP_RESPONSE + "\nPress Enter to Continue")
            elif choice == "2":
                self._storage.add_movie()
                input(COMP_RESPONSE + "\nPress Enter to Continue")
            elif choice == "3":
                self._storage.delete_movie()
                input(COMP_RESPONSE + "\nPress Enter to Continue")
            elif choice == "4":
                self._storage.update_movie()
                input(COMP_RESPONSE + "\nPress Enter to Continue")
            elif choice == "5":
                self._command_movie_stats()
                input(COMP_RESPONSE + "\nPress Enter to Continue")
            elif choice == "6":
                self._storage.random_movie()
                input(COMP_RESPONSE + "\nPress Enter to Continue")
            elif choice == "7":
                self._generate_website()
                input(COMP_RESPONSE + "\nPress Enter to Continue")
            else:
                print(ERROR_COLOR + "Invalid command.")
            print()
