import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("Transform PS1 Google Sheet Started")

    path_extracted = os.environ["GOOGLE_SHEET_TRANSFORM_INPUT_PATH"]
    
    df_sheets = pd.read_csv(
        f"{path_extracted}/extracted_google_sheets.csv", usecols=["Name", "Acquired"]
    )

    df_acquired_game = df_sheets[df_sheets["Acquired"] == 1.0]
    df_acquired_game = df_acquired_game.drop(columns=["Acquired"])
    df_acquired_game = df_acquired_game.drop_duplicates()

    path_transformed = os.environ["GOOGLE_SHEET_TRANSFORM_OUTPUT_PATH"]
    
    df_acquired_game.to_csv(f"{path_transformed}/transformed_ps1_google_sheet.csv")

    logger.info("Transform PS1 Google Sheet Finished")


if __name__ == "__main__":
    main()
