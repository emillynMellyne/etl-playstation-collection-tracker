import subprocess
import os


def main():
    path_datacenter = os.environ["DATACENTER"]
    path_google_sheet = os.environ["GOOGLE_SHEET"]

    subprocess.run(["python", f"{path_datacenter}/extract.py"])
    subprocess.run(["python", f"{path_datacenter}/transform.py"])
    subprocess.run(["python", f"{path_datacenter}/load.py"])

    subprocess.run(["python", f"{path_google_sheet}/extract.py"])
    subprocess.run(["python", f"{path_google_sheet}/transform.py"])
    subprocess.run(["python", f"{path_google_sheet}/load.py"])


if __name__ == "__main__":
    main()
