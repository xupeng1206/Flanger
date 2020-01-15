from flanger.app import FlangerApp

app = FlangerApp(__name__)
app.config.from_object('settings')
app.init()

if __name__ == '__main__':
    app.run(debug=True, port=8080)
