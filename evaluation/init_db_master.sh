cd ../../
python -m IoT.NewYork.init_db --drop

python -m IoT.NewYork.run &
echo $!

echo $$