# Restart-supervisor-api 
- Installing Python Modules : 
+ pip install flask flask_restful flask_httpauth xmlrpclib
- Run service : 

  +chmod +x run.py 

  +python run.py

Use restart supervisor
HELP : curl http://127.0.0.1:5000

IP : IP server supervisor

nameprocess : process supervisor

API Usage:
- Restart service :   curl http://127.0.0.1:5000/ip/nameproces --user user:password
- Add process and reload config : curl http://127.0.0.1:5000/add/ip/nameprocess --user user:password
