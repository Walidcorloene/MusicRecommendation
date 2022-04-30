
<div id="header" align="center">
  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/>
</div>

<h1>
  hey there
  <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="30px"/>
</h1>


### :woman_technologist: About Me :
- :telescope: We are Studying as a Data & AI and contributing for building Music Recommendation.

- :seedling: Exploring Technical Content Writing.
# Les membres du groupes :
-Walid KHIRDINE
-Antoine LABONNE
-Manal SAMADI


## Ressources

* Project objectives : 

## Dependencies

* Anaconda or Miniconda: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

## Setup

1. Create a new conda env named md4-api (if you haven't already) for the project in the Conda application or in the terminal:
```
conda create --name scrape-api python=3.7 
```

2. Activate the conda env (you can check your availables env with: conda env list):
```
conda activate scrape-api
```

3. Install the project python dependencies :
```
pip install -r requirements.txt
```

4. Install flask in your terminal to be able to launch it:
```
conda install -c conda-forge flask
```

5. Launch the API :
```
flask run --port=3000
```

## Development

To enable automatic re-launch of the API (hot reload) when there is a code update, launch flask like this:
```
FLASK_DEBUG=1 flask run --port=3000
```

## Database

To connect to a database, you must set the environment variable `DATABASE_URL` in the .env file with a valid connection URI.

Example of PostgreSQL uri:
```
DATABASE_URL=postgresql://user:password@database_host:database_port/database_name
```

To apply the database migrations (located in migrations/versions), you can use this command:
```
flask db upgrade
```

To create a new migration, you can use this command and then apply the previous command:
```
flask db migrate -m "Migration message"
```

If your database is empty and you want some random data to start working with your API, you can use this command:
```
flask seed
```
It will fill your database with a test user.

## OpenFoodFacts API
-- product_name
-- brands
-- nutriscore_grade
