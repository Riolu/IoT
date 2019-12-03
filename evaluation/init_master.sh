cd ../../
python -m IoT.UnitedStates.init_db
python -m IoT.NewYork.init_db
python -m IoT.Columbia.init_db
python -m IoT.MTA.init_db

python -m IoT.UnitedStates.run &
python -m IoT.NewYork.run &
python -m IoT.Columbia.run &
python -m IoT.MTA.run &
