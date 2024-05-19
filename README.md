# ETL PlayStation 1 Collection Tracker

An ETL to extract and track PlayStation1 games of an collection.


# Description
PS1 games are extracted from the PlayStation Datacenter  website ([https://psxdatacenter.com/ntsc-u_list.html](https://psxdatacenter.com/ntsc-u_list.html)) using web scraping with the BeautifulSoup library. The data is then stored in a SQLite database using SQLAlchemy for the creation and population of the tables.

The database stores the following information:

-   Game names
-   Disc codes for each game
-   Number of discs each game has
-   Language(s) in which each game was released

Additionally, the names of the games acquired by a hypothetical collector are extracted from a Google Sheets spreadsheet using the gspread API and cross-referenced with the games from the PlayStation Datacenter.

# Getting Started

## Setup

### Google Sheets Acquired Games List
We need to setup a GoogleSheets SpreadSheet that will store the acquired games. This Google Sheets needs to follow this model: 

![Google Sheets spreadsheet example](img/Screenshot_1.png)

- A column containing the name of game and another containing "1" for the acquired ones or blank if not acquired. 

You also need to generate an `credentials.json` file for authentication with Google. You can do it by following this tutorial [here](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account).

## Requirements

The requirements are described on the `requirements.txt` file.

It's advised to run this project using Docker.

## Environment Variables
The following environment variables are required. 

"DATACENTER_EXTRACT_OUTPUT_PATH":"data/extracted",
"DATACENTER_TRANSFORM_INPUT_PATH":"data/extracted",
"DATACENTER_TRANSFORM_OUTPUT_PATH":"data/transformed",
"DATACENTER_LOAD_INPUT_PATH":"data/transformed",
"DATACENTER_LOAD_DATABASE_PATH":"data/database",
"GOOGLE_SHEET_CREDENTIALS_PATH":"data/credentials/credentials.json",
"GOOGLE_SHEET_EXTRACT_OUTPUT_PATH":"data/extracted",
"GOOGLE_SHEET_TRANSFORM_INPUT_PATH":"data/extracted",
"GOOGLE_SHEET_TRANSFORM_OUTPUT_PATH":"data/transformed",
"GOOGLE_SHEET_LOAD_INPUT_PATH":"data/transformed",
"GOOGLE_SHEET_LOAD_DATABASE_PATH":"data/database"

Important: 
- The extracted and transformed directories will contain the data extracted and transformed by the ETL. 
- You will need to fill `GOOGLE_SHEET_CREDENTIALS_PATH` with the credentials.json file for authentication that you generated before.

## Executing
We have two methods for running this project. The first one is using the `run.sh` file and the other one is using Airflow. We will briefly describe both of them next. 

### Using `run.sh` file
The `run.sh` will build the Dockerfile of this project and automatically run all the scripts of the project. The final result will be a SQLite Database containing all the structure of the project. 

Keep in mind that you will need to create a `.env` file in the root of the project containing the environment variables describled above.

### Using Airflow
We also makes available an Airflow DAG. You can find it in the `dags` folder. It uses DockerOperator to run all the tasks of this project.

![Airflow graph of the DAG](img/Screenshot_1.png)


