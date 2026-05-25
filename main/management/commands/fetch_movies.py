import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from main.models import Genre, Movie

class Command(BaseCommand):
    help = 'Команда заполнения базы данных фильмами со стороннего сервиса'
    MOVIES = [
    ("The Shawshank Redemption", 1994), ("The Godfather", 1980), ("The Dark Knight", 2008),
    ("Pulp Fiction", 1994), ("Schindler's List", 1993), ("The Lord of the Rings: The Return of the King", 2003),
    ("Fight Club", 1999), ("Forrest Gump", 1994), ("Inception", 2010),
    ("The Matrix", 1999), ("Goodfellas", 1990), ("The Silence of the Lambs", 1991),
    ("Se7en", 1995), ("Interstellar", 2014), ("Parasite", 2019),
    ("The Green Mile", 1999), ("Gladiator", 2000), ("Saving Private Ryan", 1998),
    ("Django Unchained", 2012), ("The Prestige", 2006), ("The Departed", 2006),
    ("Whiplash", 2014), ("The Lion King", 1994), ("Back to the Future", 1985),
    ("Terminator 2: Judgment Day", 1991), ("Alien", 1986), ("Blade Runner", 1982),
    ("Die Hard", 1988), ("Jurassic Park", 1993), ("The Big Lebowski", 1998),
    ("No Country for Old Men", 2007), ("There Will Be Blood", 2007), ("Eternal Sunshine of the Spotless Mind", 2004),
    ("Memento", 2000), ("The Truman Show", 1998), ("American Beauty", 1999),
    ("Fargo", 1996), ("Reservoir Dogs", 1992), ("The Usual Suspects", 1995),
    ("L.A. Confidential", 1997), ("Heat", 1995), ("Casino", 1995),
    ("Scarface", 1983), ("The Shining", 1980), ("A Beautiful Mind", 2001),
    ("Requiem for a Dream", 2000), ("Trainspotting", 1996), ("Snatch", 2000),
    ("Lock, Stock and Two Smoking Barrels", 1998), ("Oldboy", 2003), ("Amélie", 2001),
    ("Spirited Away", 2001), ("Princess Mononoke", 1997), ("My Neighbor Totoro", 1988),
    ("Grave of the Fireflies", 1988), ("The Social Network", 2010), ("Mad Max: Fury Road", 2015),
    ("Joker", 2019), ("Avengers: Endgame", 2019), ("Spider-Man: Into the Spider-Verse", 2018),
    ("Get Out", 2017), ("La La Land", 2016), ("Arrival", 2016),
    ("The Wolf of Wall Street", 2013), ("Inglourious Basterds", 2009), ("WALL-E", 2008),
    ("Up", 2009), ("Toy Story", 1995), ("Finding Nemo", 2003),
    ("Monsters, Inc.", 2001), ("The Incredibles", 2004), ("Ratatouille", 2007),
    ("Coco", 2017), ("Inside Out", 2015), ("Zootopia", 2016),
    ("Soul", 2020), ("Everything Everywhere All at Once", 2022), ("Oppenheimer", 2023),
    ("Dune", 2021), ("The Batman", 2022), ("Top Gun: Maverick", 2022),
    ("Barbie", 2023), ("John Wick", 2014), ("The Grand Budapest Hotel", 2014),
    ("Hereditary", 2018), ("Midsommar", 2019), ("The Lighthouse", 2019),
    ("1917", 2019), ("Tenet", 2020), ("No Time to Die", 2021),
    ("Spider-Man: No Way Home", 2021), ("Black Panther", 2018), ("The Irishman", 2019),
    ("Once Upon a Time in Hollywood", 2019), ("Ford v Ferrari", 2019), ("Logan", 2017),
    ("Deadpool", 2016), ("Guardians of the Galaxy", 2014), ("Iron Man", 2008),
    ("The Avengers", 2012), ("The Dark Knight Rises", 2012),
    ("Braveheart", 1995), ("Titanic", 1997), ("The Sixth Sense", 1999),
    ("Rocky", 1976), ("The Terminator", 1984), ("Predator", 1987),
    ("The Thing", 1982), ("First Blood", 1982), ("RoboCop", 1987),
    ("Ghostbusters", 1984), ("E.T. the Extra-Terrestrial", 1982),
    ("Raiders of the Lost Ark", 1981), ("Star Wars", 1977),
    ("The Empire Strikes Back", 1980), ("Return of the Jedi", 1983),
    ("Jaws", 1975), ("Close Encounters of the Third Kind", 1977),
    ("2001: A Space Odyssey", 1968), ("A Clockwork Orange", 1971),
    ("Full Metal Jacket", 1987), ("Apocalypse Now", 1979), ("Platoon", 1986),
    ("The Deer Hunter", 1978), ("One Flew Over the Cuckoo's Nest", 1975),
    ("Taxi Driver", 1976), ("Raging Bull", 1980),
    ("The Good, the Bad and the Ugly", 1966), ("Once Upon a Time in the West", 1968),
    ("Unforgiven", 1992), ("Dances with Wolves", 1990),
    ("The Last of the Mohicans", 1992), ("The Revenant", 2015),
    ("The Martian", 2015), ("Gravity", 2013),
    ("Avatar", 2009), ("District 9", 2009), ("Children of Men", 2006),
    ("Minority Report", 2002), ("A.I. Artificial Intelligence", 2001),
    ("Blade Runner 2049", 2017), ("Ex Machina", 2015), ("Her", 2013),
    ("Gattaca", 1997), ("The Fifth Element", 1997),
    ("Total Recall", 1990), ("Starship Troopers", 1997),
    ("Groundhog Day", 1993),
]
    API_KEY = settings.OMDB_API_KEY

    def handle(self, *args, **options):
        for title, year in Command.MOVIES:
            response = requests.get(f'http://www.omdbapi.com/?t={title}&y={year}&apikey={Command.API_KEY}')
            movie_data = response.json()
            if movie_data.get('Response') != 'True':
                continue
            rating_str = movie_data.get('imdbRating', 'N/A')
            rating = float(rating_str) if rating_str != 'N/A' else None
            movie, _ = Movie.objects.update_or_create(
                title=movie_data['Title'],
                defaults={
                    'description': movie_data.get('Plot', ''),
                    'release_year': int(movie_data.get('Year', 0)) if movie_data.get('Year', '').isdigit() else None,
                    'poster_url': movie_data.get('Poster', ''),
                    'rating': rating,
                    'director': movie_data.get('Director', ''),
                    'actors': movie_data.get('Actors', ''),
                    'runtime': movie_data.get('Runtime', ''),
                    'country': movie_data.get('Country', ''),
                }
            )
            genre_string = movie_data.get('Genre', '')
            for genre_name in genre_string.split(','):
                genre_name = genre_name.strip()
                if genre_name:
                    genre, _ = Genre.objects.update_or_create(name=genre_name)
                    movie.genres.add(genre)
            
        self.stdout.write(self.style.SUCCESS(f'Добавлено {Movie.objects.count()} фильмов, {Genre.objects.count()} жанров'))
