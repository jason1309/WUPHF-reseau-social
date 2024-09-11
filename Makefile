export FLASK_APP=index.py

run:
	flask run

runDebug:
	flask  --app index.py --debug run