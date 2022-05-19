from flask import *
from settings import SECRET_KEY
from api.bookingApi import bookingAPI
from api.offerApi import offerAPI
from api.userApi import userAPI
from api.orderApi import orderAPI

app=Flask(__name__)
app.register_blueprint(bookingAPI)
app.register_blueprint(offerAPI)
app.register_blueprint(userAPI)
app.register_blueprint(orderAPI)

app.secret_key = SECRET_KEY

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login")
def login():
	return render_template("logIn.html")

@app.route("/offer")
def offer():
	return render_template("offer.html")

@app.route("/card/<id>")
def signUpCrditCard(id):
	return render_template("card.html")

@app.route("/signup")
def signup():
	return render_template("signUp.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/member")
def member():
	return render_template("member.html")

@app.route("/order/<id>")
def order(id):
	return render_template("order.html")

@app.route("/thankyou/<id>")
def thankyou(id):
	return render_template("thankyou.html")

@app.route("/alter/<id>")
def alter(id):
	return render_template("alter.html")


# 開發
# if __name__ == '__main__':
#     app.run(port=3000, debug=True)

# # 上線
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)