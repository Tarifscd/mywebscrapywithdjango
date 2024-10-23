# mywebscrapywithdjango

1. First active venv and install from requirements.txt .
2. Then add the postgres db in settings and migrate, then makemigrations and again migrate.
3. run - 'python3 manage.py scrapping_test-1' - for scrapping data download from website.
4. then run - 'python3 manage.py runserver'
5. User registration api - '<base_url>/users/register/', post, fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
6. login api - '<base_url>/users/login/', post, fiels = (username and password), and get Bearer token.
   Then use the token for next calls.
7. Save downloaded data into database - '<base_url>/scrap/data/save/', post, no request body required, just {}.
8. Update data into database - '<base_url>/scrap/data/update/', post, fields = {"id": 5, "data_type": ".pdf","published_date": "2024-10-23", 
"path": "/dghfhg/vbbb/bbbb"}

