echo $$

itrs=10

start_time="$(date -u +%s.%N)"
for ((i=1;i<=itrs;i++)); do
    JSON=\''{"targetLoc":"level5", "td":{"_type": "pc", "id": "'"urn:dev:ops:54312-pc-$i"'"}}'\'
    echo "$JSON"
    cmd=\''curl http://192.168.1.189:5000/register -X POST -d '"$JSON"' -H "Content-Type:application/json"'\'
    echo "$cmd"
    eval $cmd
    # td=\''{"_type": "pc", "id": "'"$i"'"}'\'
    # JSON=\''{"targetLoc": "level5", "td": "'"$td"'"}'\'
    # echo "$JSON"
    # curl http://192.168.1.189:5000/register -X POST -d "$JSON" -H "Content-Type:application/json"
done
end_time="$(date -u +%s.%N)"

elapsed="$(bc <<< "$end_time-$start_time")"
echo "Total of $elapsed seconds elapsed for zzz"
echo "Average time: $(bc -l <<< "$elapsed/$itrs")"

# curl http://192.168.1.189:5000/register -X POST -d '{"targetLoc":"level5", "td":{"_type": "pc", "id": "urn:dev:ops:54312-pc-$i"}}' -H "Content-Type:application/json"

# td=\''{"_type": "pc", "id": "'"$i"'"}'\'
# JSON=\''{"targetLoc": "level5", "td": "'"$td"'"}'\'
