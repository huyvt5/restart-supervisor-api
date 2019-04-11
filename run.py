rom __future__ import print_function # In python 2.7
from flask import Flask
from flask import jsonify
from flask import abort, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
import xmlrpclib
import sys
app = Flask(__name__)
auth = HTTPBasicAuth()
help_message = """
API Usage:

- Restart service :   curl http://127.0.0.1:5000/ip/nameproces --user user:password
- Add process and reload config : curl http://127.0.0.1:5000/add/ip/nameprocess --user user:password

"""
## Help
@app.route('/', methods=['GET'])
def help():
    return help_message
## Username Password
users = {
    "admin": "abcd1234"
}
## Check Password
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

### Restart superviosr
@app.route('/<ipserver>/<nameprocess>')
@auth.login_required
def RestartService(ipserver,nameprocess):
    if request.remote_addr == '127.0.0.1': #Allow IP connect
        info_server = 'http://{0}:9001/RPC2'.format(ipserver,nameprocess)
        nameprocess = '{1}'.format(ipserver,nameprocess)
        server = xmlrpclib.Server(info_server)
        if server.supervisor.getProcessInfo(nameprocess)['statename'] == "STOPPED":
            server.supervisor.startProcess(nameprocess)
            return "Restarted Service {1} in {0}".format(ipserver,nameprocess)
        else:
            server.supervisor.stopProcess(nameprocess)
            server.supervisor.startProcess(nameprocess)
            return "Restarted Service {1} in {0}".format(ipserver,nameprocess)
### Add process superviosr
@app.route('/add/<ip>/<process>')
@auth.login_required
def AddService(ip,process):
    if request.remote_addr == '127.0.0.1': #Allow IP connect
        info_server = 'http://{0}:9001/RPC2'.format(ip,process)
        nameprocess = '{1}'.format(ip,process)
        server = xmlrpclib.Server(info_server)
        data = server.supervisor.getAllProcessInfo()
        check = 'false'
        for process_name in data:
            print(process_name['name'], file=sys.stderr)
            if nameprocess == process_name['name']:
                check = 'false'
                break
            else:
                check = 'true'
        if check == 'true':
            server.supervisor.reloadConfig()
            server.supervisor.addProcessGroup(nameprocess)
            return "Added and Started"+" "+nameprocess+" "+"in {0}".format(ip,process)
        else:
            return "Already"+" "+nameprocess+" "+"in {0}".format(ip,process)
if __name__ == '__main__':
    app.run(debug=True)
