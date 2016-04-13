# PTP - Pirate Trading Platform

# Install

    ./install.sh

## Manual Install
### Download redis

    wget http://redis.googlecode.com/files/redis-1.2.5.tar.gz
    tar -xvf redis-1.2.5.tar.gz
    rm redis-1.2.5.tar.gz
    cd redis-1.2.5
    make
    
### Config redis port to 6669
		
    cd redis-1.2.5
    cp redis.conf redis2.conf
    cat redis2.conf | sed ’s/6367/6669/g’ > redis.conf
    rm redis2.conf

### Install pip requirements

    pip install -r requirements.txt
    
### Log into Robinhood

    python make-keys.py

# Using

	./launch 'stock'
	./launch 'TWTR'
        
# In case of emergency
	
	./manual-shutoff
        
# Download data for analysis
RUN is default 1.

	python download-db-csv.py RUN STOCK
	eg. python download-db-csv.py 1 'TWTR'
