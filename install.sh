# Download redis
wget http://redis.googlecode.com/files/redis-1.2.5.tar.gz
tar -xvf redis-1.2.5.tar.gz
		rm redis-1.2.5.tar.gz
cd redis-1.2.5
make

# Config redis port to 6669		
cp redis.conf redis2.conf
cat redis2.conf | sed "s/6379/6669/g" > redis.conf
rm redis2.conf
cp redis.conf redis2.conf
cat redis2.conf | sed "s/daemonize no/daemonize yes/g" > redis.conf
rm redis2.conf

# install python requirements with pip
cd ..
pip install -r requirements.txt

# key configure
python make-keys.py