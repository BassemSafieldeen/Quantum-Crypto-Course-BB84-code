
ps aux | grep python | grep Test | awk {'print $2'} | xargs kill -9

python Alice.py &
python Bob.py &
python Eve.py &
