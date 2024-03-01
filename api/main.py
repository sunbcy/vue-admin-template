from app import create_app
app = create_app()

@app.route("/")
def index():
  return app.send_static_file('index.html')

if __name__ == '__main__':
	app.run(port=5000, host='0.0.0.0')