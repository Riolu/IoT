cd ../../
python -m IoT.UnitedStates.init_db --drop
python -m IoT.NewYork.init_db --drop
python -m IoT.Columbia.init_db --drop
python -m IoT.MTA.init_db --drop

python -m IoT.UnitedStates.run &
echo $!
python -m IoT.NewYork.run &
echo $!
python -m IoT.Columbia.run &
echo $!
python -m IoT.MTA.run &
echo $!

echo $$