from ..src.app import getApp

if __name__ == '__main__':
    app = getApp('level5')
    app.run(host='0.0.0.0', port=5004)