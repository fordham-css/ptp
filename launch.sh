./redis-1.2.5/redis-server ./redis-1.2.5/redis.conf
#python vis-api-server.py $1
python manager.py $1
pkill 'redis-server'
rm *.pyc
rm *.sh~
