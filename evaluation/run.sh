start_time="$(date -u +%s.%N)"
for i in {1..100}
do
    curl http://192.168.1.189:5000/register -X POST -d '{"targetLoc":"columbia", "td":{"_type": "pc", "id": "urn:dev:ops:54312-pc-$(i)"}}' -H "Content-Type:application/json"
done
end_time="$(date -u +%s.%N)"

elapsed="$(bc <<<"$end_time-$start_time")"
echo "Total of $elapsed seconds elapsed for zzz"
echo "Average time: $((elpased/10))"