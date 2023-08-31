import os
from app import create_app
from flask_script import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default') 
# run_with_ngrok(app)
manager = Manager(app)
manager.add_command('runserver', Server(host="192.168.43.73", threaded=True, port=200))


if __name__ == '__main__':   
    manager.run()


