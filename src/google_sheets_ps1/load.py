import sqlite3
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    inspect,
    create_engine,
    select,
)
import logging
import pandas as pd
import os
from utils import create_table, insert_values

logger = logging.getLogger(__name__)


def main():
    logger.info("Load PS1 Google Sheet Started")
    logging.basicConfig(level=logging.INFO)

    path_transformed = os.environ["GOOGLE_SHEET_LOAD_INPUT_PATH"]
    
    df_game_acquired = pd.read_csv(
        f"{path_transformed}/transformed_ps1_google_sheet.csv", usecols=["Name"]
    )

    path_database = os.environ["GOOGLE_SHEET_LOAD_DATABASE_PATH"]
    
    conn_sqlite = sqlite3.connect(f"{path_database}/database.db")
    engine = create_engine(f"sqlite:///{path_database}/database.db", echo=True)

    metadata = MetaData()

    game_acquired = Table(
        "Game_Acquired",
        metadata,
        Column("Name", String),
    )  
    create_table(engine, metadata)

    rows_to_insert = []
    for index, row in df_game_acquired.iterrows():
        rows_to_insert.append(
            {
                "Name": row["Name"],
            }
        )
    insert_values(game_acquired, engine, rows_to_insert)

    logger.info("Load PS1 Google Sheet Finished")


if __name__ == "__main__":
    main()
