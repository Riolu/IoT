cd ../../
python -m IoT.NYState.init_db --drop
python -m IoT.Manhattan.init_db --drop

python -m IoT.NYState.run &
echo $!
python -m IoT.Manhattan.run &
echo $!

echo $$