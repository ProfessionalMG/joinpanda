# Backend Developer Test

## Installation

Clone this Repository

```bash
git clone https://github.com/ProfessionalMG/joinpanda.git
cd joinpanda
```

Install dependencies

```bash
pip install -r requirements.txt
```

Ensure that your .env file is properly configured. (connection to a postgres database)

Run Migrations

```bash
python manage.py migrate
```

Once migrations have been run you can start the server

```bash
python manage.py runserver
```

## End Points:

`http://127.0.0.1:8000/api/processFile/` - Allowed methods POST
accepts a csv file where in the body of the request you must attach the csv file with the key of file.
the site will parse through the `file` to validate the data and save it to the database.
The value for Net has an extra value for converted Net meaning the value in this column is the value of the purchase in
euros as the instructions called for the currency column to be converted to Euros which I suspect was an error.
This conversion is done by fetching the exchange rate using the European Central Banks API.

`http:127.0.0.1:8000/api/retrieveRows/` - Allowed methods GET
which takes in the following query parameters
country - which must be in ISO 3166 Format
date - which must be in the format YYYY/MM/DD

## Limitations

Processing time: The App is very slow at uploading files

On upload the app doesn't return any failed rows to user. Either the whole thing works or it doesn't.

When retrieving rows the app doesn't give an appropriate failing response.

## Scaling

I would save exchange rate Data to the db to speed up the currency conversion process as it is very lengthy.
Additionally, I would standardise the country names that are saved in the db. Possibly create a new model that has the
county name and code saved. Another alternative would be to use a third partly library like pycountry to try and resolve
this step.