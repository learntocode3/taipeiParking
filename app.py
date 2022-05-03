from flask import *
from settings import SECRET_KEY
from api.bookingApi import bookingAPI

app=Flask(__name__)
app.register_blueprint(bookingAPI)

app.secret_key = SECRET_KEY

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")


# 開發
if __name__ == '__main__':
    app.run(port=3000, debug=True)

# # 上線
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=3000)