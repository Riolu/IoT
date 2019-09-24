from eve import Eve
app = Eve()

@app.route("/exp")
def get_exp():
    return "hello world"

if __name__ == '__main__':
    app.run()
    