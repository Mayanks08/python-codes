import os 
import json

FILENAME = "my_movies.json"

def load_movies():
    if not os.path.exists(FILENAME):
        return [],
    with open(FILENAME, 'r' ,encoding="utf-8") as f:
        return json.load(f)

def save_movies(movies):
    with open(FILENAME, 'w', encoding="utf-8") as f:
        json.dump(movies, f, indent=4)

def add_movies(movies):
    title = input("Movie title: ").strip().lower()
    
    if any(movie['title'].lower() == title for movie in movies):
        print("Movie already exist")
        return
    genre=input('Genre:').strip().lower()
    try:
        rating = float(input('Rating(0-10)').strip())
        if not (0<=rating<=10):
            print("Rating must be between 0 and 10")
            return
    except ValueError:
        print("Rating must be a number")
        return
    year_str=input("Year:").strip()
    try:
        year=int(year_str)
        if not (1800 <= year <=2026):
            print("Year must be between 1800 and 2026")
            return
    except ValueError:
        print("Year must be a valid year")
        return

    movies.append({"title":title, "genre":genre, "rating":rating, "year":year})
    save_movies(movies)
    print("Movie added successfully")

def search_movies(movies):
    term = input("Enter the title or genre to search:").strip().lower()  

    found = [movie for movie in movies if 
        term in movie['title'].lower() or 
        term in movie['genre'].lower()
    ]
    if not results:
        print("No movie found")
        return
    print(f" Found {len(results)} results")

    results = None
    for movie in results:
        print(f"Title {movie['title']}")
        print(f"Genre {movie['genre']}")
        print(f"Rating {movie['rating']}")
        print(f"Year {movie['year']}")
        print()

def delete_movie(movies):
    title = input("Enter the title to delete: ").strip().lower()
    initial_len = len(movies)
    movies = [movie for movie in movies if movie['title'].lower() != title]
    
    if len(movies) == initial_len:
        print("Movie not found.")
    else:
        save_movies(movies)
        print("Movie deleted successfully.")
    return movies

def stats_movies(movies):
    if not movies:
        print("No movies in list.")
        return
    
    total = len(movies)
    avg_rating = sum(m['rating'] for m in movies) / total
    
    genres = {}
    for m in movies:
        g = m['genre']
        genres[g] = genres.get(g, 0) + 1
        
    print("\n=== Statistics ===")
    print(f"Total movies: {total}")
    print(f"Average rating: {avg_rating:.1f}")
    
    print("\nBy Genre:")
    for g, c in genres.items():
        print(f"{g.title()}: {c}")




def main():
    movies = load_movies()
    
    while True:
        print("\n===== Movie Tracker =====")
        print("1. Add Movie")
        print("2. View All Movies")
        print("3. Search Movies")
        print("4. Delete Movie")
        print("5. Statistics")
        print("6. Exit")
        
        choice = input("Choose an option: ").strip()
        
        if choice == '1':
            add_movies(movies)
        elif choice == '2':
            if not movies:
                print("No movies added yet.")
            else:
                for movie in movies:
                    print(f"Title: {movie['title']}")
                    print(f"Genre: {movie['genre']}")
                    print(f"Rating: {movie['rating']}")
                    print(f"Year: {movie['year']}")
                    print("-" * 20)
        elif choice == '3':
            search_movies(movies)
        elif choice == '4':
            movies = delete_movie(movies)
        elif choice == '5':
            stats_movies(movies)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

        
