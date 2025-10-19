# Tietokannat-ja-web-ohjelmointi-projekti / Bar reviewer

A program to chart bars/restaurants.

- Users can explore added locations and the draft drinks that are served there.
- Users can register, log in, log out.
- Users can add comments to locations.
- Users can edit and delete their comments.
- Users can search for locations or comments with keywords.
- Users can add new locations, their addresses, names, served draft drinks, extra info and benefits.
- Users can see added locations and the comments under that location. 
- Users can explore other user profiles.
- Users can edit and delete locations.



Under construction:
- Adding a rating system (1-5 stars) to locations.
- user ratings
- some other data like avg.rating on bars and even users.
- visuals, clarity
- favourite bars
- following other users
- sort by price,location,rating
- original idea of having a map. google map/api?
- picture functionality on locations/ front



--------------------------------------------------------------------------------------------
Instructions on installing the program:

1. Download or clone the project files
2. Navigate to the program folder:
   - terminal: cd "path/to/yourfolder"
4. Create and activate virtual environment:
   - terminal: python3 -m venv venv
5. Activate virtual environment:
   - terminal: source venv/bin/activate
6. Install flask if not installed yet:
   - terminal: pip install flask
7. Create database:
   - terminal: sqlite3 database.db < schema.sql
8. Optionally add example data seed (recommended):
   - terminal: sqlite3 database.db < seed.sql
9. Run the application:
   - flask run
10. Access in browser with the provided address (usually 127.0.0.1:5000)

For future launch of application, you may go through the following steps:
2 --> 5 --> 9 --> 10



