from ..src.app import getApp

if __name__ == '__main__':
    app = getApp('columbia')
    app.run(host='0.0.0.0', port=5004)
