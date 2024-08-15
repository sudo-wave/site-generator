export $(grep -v '^#' .env | xargs)
python3 -m unittest discover -s tests
