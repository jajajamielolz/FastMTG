No longer being maintained - initial project to learn Fast API
goal of the app is to archive a collection of magic the gathering cards, and use `mtgsdk` to build a 99 card commander decks around an initial commander card. 


# Fast_Blocksci
Fast API app to query mtg stuff

### Swagger 
for interactive swagger docs go to http://localhost:8000/docs


### Formatting
flake8, black, and reorder python imports are used for formatting, set up pre-commit hooks with `pre-commit install`
and run reformatting with `pre-commit run --all-files`

### Alembic & SQLite3
This repo is using alembic to handle schema migrations and using SQLite3 for a database. To initialize your local db run `alembic upgrade head`

Once any model files are added, auto generate a migration script with `alembic revision --autogenerate -m "<short revision description>"`

## Testing
The testing environment is automatically configured with the `.env.testing` file (see `app/config.py` for more information). Since these are testing credentials, we can keep in plain text and checked into the repository.

To run the entire test suite, just run `pytest`!
```
pytest
```



### Global Fixtures and Writing Tests
There are a number of useful pytest fixtures defined in `app/conftest.py`.

**client**: This fixture returns a fast test client

```
client.get("example/route/")
```

**test_db**: This fixture gives access to a temporary sql database that can be connected to in the same way as a 
standard database.

**tempdir**: A temporary directory that is reset for each test function.
