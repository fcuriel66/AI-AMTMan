from sqlalchemy.exc import SQLAlchemyError
from models import db, User, Aircraft, Service, Request, FetchedTask
import requests
import os
from dotenv import load_dotenv

# Keeping the API_KEY secure
load_dotenv()
#OMDB_API_KEY = os.getenv('OMDB_API_KEY')

class DataManager:
    # CRUD ops (as methods)
    def create_user(self, name: str) -> User:
        """
        Create/add user to database. Returns new user or None.
        """
        try:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return None


    def get_users(self):
        """
        Gets all users from database
        Returns: all users or empty list if no users exist
        """
        try:
            return User.query.all()
        except SQLAlchemyError as e:
            print(f"Error while retrieving users: {e}")
            return []


    # def get_movies(self, user_id: int) -> list[Movie]:
    #     """ Return all movies linked to a user or [] if not """
    #     try:
    #         return Movie.query.filter_by(user_id = user_id).all()
    #     except SQLAlchemyError as e:
    #         print(f"Error while retrieving movies for user: {user_id}: {e}")
    #         return []
    #
    #
    # def add_movie(self, title, user_id: int) -> Movie:
    #     """
    #     Add movie to database. Returns new movie or None.
    #     """
    #     try:
    #         response = requests.get(f'https://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}')
    #         data = response.json() # jsonify response to be able to work with info as a dictionary
    #
    #         if data['Response'] == 'True':
    #             new_movie = Movie(
    #                 name = data["Title"],
    #                 director = data["Director"],
    #                 year = int(data["Year"]),
    #                 poster_url = data["Poster"],
    #                 user_id=user_id
    #             )
    #
    #             db.session.add(new_movie)
    #             db.session.commit()
    #             return new_movie
    #         else:
    #             raise ValueError(f' {data['Error']} (in OMDB API)') ####
    #     except SQLAlchemyError as e:
    #         db.session.rollback()
    #         print(e)
    #         return None
    #
    #
    # def update_movie(self, movie_id: int, user_id: int, new_title: str) -> Movie:
    #     """
    #     Update movie from database. Returns movie with updated title or None
    #     """
    #     try:
    #         movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
    #         if movie:
    #             movie.name = new_title  # For now, updates only the movie title
    #             db.session.commit()
    #             return movie
    #         else:
    #             raise ValueError(f"Movie with ID {movie_id} not found.")
    #     except SQLAlchemyError as e:
    #         db.session.rollback()
    #         print(f"Error while updating movie: {movie_id}: {e}")
    #         return None
    #
    #
    # def delete_movie(self, user_id:int, movie_id:int) -> bool:
    #     """ Delete a movie only if linked to a user """
    #     try:
    #         movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
    #         if movie:
    #             db.session.delete(movie)
    #             db.session.commit()
    #             return  True
    #         else:
    #             print(f"Movie with id {movie_id} not found.")
    #             return False
    #     except SQLAlchemyError as e :
    #         print(f"Error deleting movie {e}")
    #         return False

