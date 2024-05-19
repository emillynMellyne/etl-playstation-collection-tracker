docker build -t dockerps1:latest .;

docker run --rm --env-file .env -v /path/to/your/data/folder:/app/data --name containerps1 dockerps1:latest python src/datacenter_ps1/extract.py;
docker run --rm --env-file .env -v /path/to/your/data/folder:/app/data --name containerps1 dockerps1:latest python src/datacenter_ps1/transform.py;
docker run --rm --env-file .env -v /path/to/your/data/folder:/app/data --name containerps1 dockerps1:latest python src/datacenter_ps1/load.py;

docker run --rm --env-file .env -v /path/to/your/data/folder:/app/data --name containerps1 dockerps1:latest python src/google_sheets_ps1/extract.py;
docker run --rm --env-file .env -v /path/to/your/data/folder:/app/data --name containerps1 dockerps1:latest python src/google_sheets_ps1/transform.py;
docker run --rm --env-file .env -v /path/to/your/data/folder:/app/data --name containerps1 dockerps1:latest python src/google_sheets_ps1/load.py;



