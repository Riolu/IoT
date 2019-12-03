from ..src.app import getApp

if __name__ == '__main__':
    app = getApp('new_york_state')
    app.run(host='0.0.0.0', port=5001)
