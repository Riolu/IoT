from ..src.app import getApp

if __name__ == '__main__':
    app = getApp('level4')
    app.run(host='0.0.0.0', port=5003)