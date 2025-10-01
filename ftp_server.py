import os
import click
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Must create deault vault first
DEFAULT_VALUT="./res"

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
        # print(len(file))
        pass

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        import os
        os.remove(file)

@click.command()
@click.option('--username', '-u', default='123', help='[u]sername for authorize')
@click.option('--password', '-p', default='123', help='[p]assword for authorize')
@click.option('--host', '-h', default='172.20.10.13', help='[h]ostname of server')
@click.option('--port', default=21 ,help='port of service')
@click.option('--fpath', default=DEFAULT_VALUT, help='resource folder location')
def serve(username, password, host, port, fpath):
    print("Start FTP server...")
    if not os.path.isdir(fpath):
        os.makedirs(fpath)
    
    authorizer = DummyAuthorizer()
    authorizer.add_user(username, password, fpath, perm="elradfmwMT")
    authorizer.add_anonymous("./anonymous")

    handler = FTPHandler
    handler.authorizer = authorizer

    try:
        server = FTPServer((host, port), handler)
        server.serve_forever()
    except Exception as e:
        print(e)
    
    # TODO get target file length
    # TODO add simple progress bar for checkout file tranfer
 

if __name__ == "__main__":
    serve()
