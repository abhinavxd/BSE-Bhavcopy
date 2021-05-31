# BSE-Bhavcopy Search and Import 

### BSE publishes a "Bhavcopy" (Equity) ZIP every day at 18:00 IST here: https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx

This application runs a Django command daily at 18:00 IST and automatically downloads, extracts zip file in memory and imports BhavCopy csv data into appropriate REDIS data structure, And also makes this data searchable.

Plus you can download the results as CSV. 

* API Endpoints
	
      https://bsebhavcopy.abhinavr.me/api/search-prefix

      https://bsebhavcopy.abhinavr.me/api/get-data-by-name
      
### Deployment instructions

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
      
* MAKE SURE YOUR virtual environment name is 'venv' 
    
* Install node from https://nodejs.org/en/ and build frontend 

      cd frontend
      npm install
      npm run build

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
       
### Steps to run daily import Django command from bash file in background
       
       cd jobs/
       sudo nohup ./download_bhavcopy.sh &
       
       Press CTRL + C to close (now the bash file is running in background)
       
       To check if it's running run the following:
       ps -fe | grep -i bhavcopy
 
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
 
       
 
