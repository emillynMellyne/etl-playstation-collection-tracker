import pandas as pd
import logging
import re
import os

logger = logging.getLogger(__name__)


def separate_into_lines(text, regex):
    results = re.findall(regex, text)
    return results


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("Transform PS1 DataCenter Started")

    path_transform = os.environ["DATACENTER_TRANSFORM_INPUT_PATH"]
    
    df_transform = pd.read_csv(
        f"{path_transform}/extracted_ps1_datacenter.csv",
        usecols=["Disk_Code", "Name", "Language"],
    )
    df_transform = df_transform.drop_duplicates()
    df_transform = df_transform.reset_index()
    df_transform = df_transform.rename(columns={"index": "Id"})

    # Each disk code is exactly 10 characters long
    df_transform["Disk_Count"] = df_transform["Disk_Code"].apply(lambda x: len(x) // 10)

    regex = r"(S[LC]US-\d{5})"
    df_transform["result"] = df_transform["Disk_Code"].apply(
        lambda x: separate_into_lines(x, regex)
    )
    df_transform = df_transform.explode("result").reset_index(drop=True)
    df_transform = df_transform.drop(columns=["Disk_Code"])
    df_transform = df_transform.rename(columns={"result": "Disk_Code"})

    df_game = df_transform[["Id", "Name", "Disk_Count", "Language"]]
    df_game = df_game.drop_duplicates()

    df_disk = df_transform[["Id", "Disk_Code"]]
    df_disk = df_disk.rename(columns={"Id": "Id_game"})

    path_transformed = os.environ["DATACENTER_TRANSFORM_OUTPUT_PATH"]
    
    df_game.to_csv(f"{path_transformed}/transformed_ps1_datacenter_game.csv")
    df_disk.to_csv(f"{path_transformed}/transformed_ps1_datacenter_disk.csv")

    logger.info("Transform PS1 DataCenter Finished")


if __name__ == "__main__":
    main()
