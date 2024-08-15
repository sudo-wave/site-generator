export $(grep -v '^#' .env | xargs)
python3 src/ssglite/main.py
cd public && python3 -m http.server 8888
