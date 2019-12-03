cd ../../
python -m IoT.NYState.init_db
python -m IoT.Manhattan.init_db

python -m IoT.NYState.run &
python -m IoT.Manhattan.run &
