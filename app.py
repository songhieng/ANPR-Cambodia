from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import auth as firebase_auth
from functools import wraps
from flask import redirect, url_for

app = Flask(__name__)

cred = firebase_admin.credentials.Certificate("./anpr-5a023-firebase-adminsdk-mrrmo-38882af9fe.json")
firebase_admin.initialize_app(cred)

def check_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('firebase_token')  
        if not token:
            return redirect(url_for('auth'))
        try:
            firebase_auth.verify_id_token(token)  # <-- Updated here
        except:
            return redirect(url_for('auth'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/admin')
@check_auth  
def admin(): 
    return render_template('admin.html')

@app.route('/map')
@check_auth  
def map(): 
    return render_template('map.html')

@app.route('/detected')
@check_auth  
def detected(): 
    return render_template('detected.html')

@app.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    try:
        decoded_token = firebase_auth.verify_id_token(token)  # <-- Updated here
        uid = decoded_token['uid']
        return jsonify({"status": "success", "uid": uid})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
