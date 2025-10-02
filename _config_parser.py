import configparser
import os

class ConfigParser:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file '{config_file}' not found")
        
        self.config.read(config_file)
    
    def get_username(self):
        return self.config.get('login', 'username', fallback='123')
    
    def get_password(self):
        return self.config.get('login', 'password', fallback='123')
    
    def get_host(self):
        return self.config.get('address', 'host', fallback='127.0.0.1')
    
    def get_port(self):
        return self.config.getint('address', 'port', fallback=21)
    
    def get_resource_path(self):
        return self.config.get('address', 'res', fallback='./res')
    
    def get_all_settings(self):
        """Returns a dictionary with all settings"""
        return {
            'username': self.get_username(),
            'password': self.get_password(),
            'host': self.get_host(),
            'port': self.get_port(),
            'fpath': self.get_resource_path()
        }