# BSE-Bhacopy Search and Import 

### BSE publishes a "Bhavcopy" (Equity) ZIP every day at 18:00 IST here: https://www.bseindia.com/markets/MarketInfo/BhavCopy.asp

### This application downloads bhavcopy from BSE website and makes it searchable and also runs a Django command daily at 18:00 and automatically downloads extracts and imports BhavCopy data into appropriate REDIS data structure.

* Update list of packages from all repositories

      sudo apt-get update
      
* Install python3 and pip dependencies

      sudo apt-get install python3-dev python-pip
      
* Install redis for your linux distribution: https://redis.io/topics/quickstart
    
      sudo apt-get install redis

* Clone the repository    

      git clone https://github.com/abhinavxd/BSE-Bhavcopy.git
      cd BSE-Bhavcopy

* Create python3 virtual environtment inside the repository root
      
      sudo apt-get install python3-venv
      python3 -m venv venv
      
      **MAKE SURE YOUR environment name is 'venv'**   
    
* Install node from https://nodejs.org/en/ and build frontend 

      cd frontend
      npm install
      
      For production:
      npm run build
      
      For dev:
      npm run dev
      
* Activate the virtual environment and install the requirements
     
      source venv/bin/activate
      pip install -r requirements.txt
      
* Create .env file inside BSE-Bhavcopy/bse_bhavcopy/ directory with following data

      REDIS_HOST=127.0.0.1
      REDIS_PORT=6379
      DEBUG=True
      SECRET_KEY=notsosecret
      
* Apply migrations
      
      python manage.py migrate

 * Run development server
 
       python manage.py runserver
 
 ### Production server deployment steps

 * Install nginx webserver https://www.nginx.com/
      
       sudo apt-get install nginx
       
 * Inside Project root folder run the following command to start gunicorn in daemon mode.       
       
       gunicorn --bind 0.0.0.0:8000 bse_bhavcopy.wsgi --daemon
       
 * Setup NGINX as reverse proxy, add following line in Server block inside file /etc/nginx/sites-available/default 
      
       location / {
		proxy_pass http://localhost:8000/ 
       }
       
 * Verify nginx configuration and reload nginx

       sudo nginx -t
       sudo nginx -s reload
 
 * If you are still having issues with NGINX read the following guide.
      
       https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

       OR 
       
       Download my nginx configuration for gunicorn server here:
       https://pastecreate.com/CPhrLu8
            
       
       
 
