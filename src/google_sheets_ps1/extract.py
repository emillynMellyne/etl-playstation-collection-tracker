import gspread
import logging
import pandas as pd
import os

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("Extract PS1 Google Sheets Started")

    credentials_filepath = os.environ["GOOGLE_SHEET_CREDENTIALS_PATH"]
    
    gc = gspread.service_account(filename=credentials_filepath)
    sh = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/1M_5n9xPJLZaNx2rPPU8SqYga2uaVTOuoUIhcrp7ZmRw/edit#gid=0"
    )

    worksheet = sh.worksheet("Página1")

    df_google_sheet = pd.DataFrame(worksheet.get_all_records())
    df_google_sheet.columns = ["Name", "Acquired"]

    path_extract = os.environ["GOOGLE_SHEET_EXTRACT_OUTPUT_PATH"]
    
    df_google_sheet.to_csv(f"{path_extract}/extracted_google_sheets.csv")

    logger.info("Extract PS1 Google Sheets Finished")


if __name__ == "__main__":
    main()
