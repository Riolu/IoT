import os

class Config:
    SECRET = os.environ.get('SECRET') or '7m689BPlHec-cRtzfoWqzQJMZ-FXMMr5ZpikX9wCljk'
    MASTER_URL = 'http://192.168.1.189:5000/'