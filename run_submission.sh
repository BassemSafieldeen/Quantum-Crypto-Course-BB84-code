
ps aux | grep python | grep Test | awk {'print $2'} | xargs kill -9

python a.py &
python b.py &
python e.py &
