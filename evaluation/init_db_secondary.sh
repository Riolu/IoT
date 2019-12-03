cd ../../
python -m IoT.Manhattan.init_db --drop
python -m IoT.Columbia.init_db --drop
python -m IoT.MTA.init_db --drop

python -m IoT.Manhattan.run &
echo $!
python -m IoT.Columbia.run &
echo $!
python -m IoT.MTA.run &
echo $!

echo $$