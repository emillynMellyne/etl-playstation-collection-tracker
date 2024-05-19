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
    logger.info("Load PS1 DataCenter Started")
    logging.basicConfig(level=logging.INFO)

    path_load = os.environ["DATACENTER_LOAD_INPUT_PATH"]
    
    df_game = pd.read_csv(
        f"{path_load}/transformed_ps1_datacenter_game.csv",
        usecols=["Id", "Name", "Disk_Count", "Language"],
    )
    df_disk = pd.read_csv(
        f"{path_load}/transformed_ps1_datacenter_disk.csv",
        usecols=["Id_game", "Disk_Code"],
    )
    
    path_database = os.environ["DATACENTER_LOAD_DATABASE_PATH"]
    
    if os.path.exists(f"{path_database}/database.db"):
        os.remove(f"{path_database}/database.db")
    
    conn_sqlite = sqlite3.connect(f"{path_database}/database.db")
    engine = create_engine(f"sqlite:///{path_database}/database.db", echo=True)
    
    metadata = MetaData()

    game = Table(
        "Game",
        metadata,
        Column("Id", Integer, primary_key=True),
        Column("Name", String),
        Column("Disk_Count", String),
        Column("Language", String),
    )

    disk = Table(
        "Disk",
        metadata,
        Column("Id_game", Integer),
        Column("Code", String),
    )
    create_table(engine, metadata)

    rows_to_insert = []
    for index, row in df_game.iterrows():
        rows_to_insert.append(
            {
                "Id": row["Id"],
                "Name": row["Name"],
                "Disk_Count": row["Disk_Count"],
                "Language": row["Language"],
            }
        )
    insert_values(game, engine, rows_to_insert)

    rows_to_insert = []
    for index, row in df_disk.iterrows():
        rows_to_insert.append(
            {
                "Id_game": row["Id_game"],
                "Code": row["Disk_Code"],
            }
        )
    insert_values(disk, engine, rows_to_insert)

    logger.info("Load PS1 DataCenter Finished")


if __name__ == "__main__":
    main()
