import os
import click
from _config_parser import ConfigParser
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class MyHandler(FTPHandler):
        
    def on_connect(self):
        print("%s:%s connected" % (self.remote_ip, self.remote_port))

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        pass

    def on_file_received(self, file):
        # do something when a file has been received
        pass

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)

@click.command()
@click.option('--username', '-u', help='[u]sername for authorize')
@click.option('--password', '-p', help='[p]assword for authorize')
@click.option('--host', '-h', help='[h]ostname of server')
@click.option('--port', help='port of service')
@click.option('--fpath', help='resource folder location')
@click.option('--config', '-c', default='config.ini', help='path to config file')
def serve(username, password, host, port, fpath, config):
    print("Start FTP server...")
    if not os.path.isdir(fpath):
        os.makedirs(fpath)
    
    # Load config file
    try:
        cfg = ConfigParser(config)
        settings = cfg.get_all_settings()
    except FileNotFoundError:
        print("Warning: Config file not found, using defaults")
        settings = {
            'username': '123',
            'password': '123',
            'host': '127.0.0.1',
            'port': 21,
            'fpath': './res'
        }
    
     # Command-line arguments override config file
    username = username or settings['username']
    password = password or settings['password']
    host = host or settings['host']
    port = port or settings['port']
    fpath = fpath or settings['fpath']
    
    authorizer = DummyAuthorizer()
    authorizer.add_user(username, password, fpath, perm="elradfmwMT")
    authorizer.add_anonymous("./anonymous")

    handler = MyHandler
    handler.authorizer = authorizer

    try:
        server = FTPServer((host, port), handler)
        server.serve_forever()
    except Exception as e:
        print(e)
    
    # TODO Auto/Scan find device addr 
    # TODO add simple progress bar for checkout file tranfer
 

if __name__ == "__main__":
    serve()
