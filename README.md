# BSE-Bhacopy 
### This application downloads bhavcopy from BSE website and makes it searchable 
### BSE publishes a "Bhavcopy" (Equity) ZIP every day at 18:00 IST here: https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx

* Update the system     

      sudo apt-get update
      
* Install base dependencies

      sudo apt-get install python3-dev python-pip
      
* Install redis for your linux distribution: https://redis.io/topics/quickstart

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
      
* Apply migrations
      
      python manage.py migrate

 * Run development server
 
       python manage.py runserver
    
 
