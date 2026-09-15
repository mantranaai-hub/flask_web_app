import os

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

# Keep credentials in environment variables.
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-change-this-key")
app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID", "")
app.config["GOOGLE_CLIENT_SECRET"] = os.getenv("GOOGLE_CLIENT_SECRET", "")

oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

def render_login(mode="login", error="", success="successfully logged into the website"):
    return render_template(
        "login.html",
        initial_auth_mode=mode,
        auth_error=error,
        auth_success=success,
        auth_routes={
            "login_action": url_for("login"),
            "signup_action": url_for("signup"),
            "google_auth_login": url_for("google_auth", flow="login"),
            "google_auth_signup": url_for("google_auth", flow="signup"),
        },
    )


@app.route("/", methods=["GET"])
def homepage():
    return render_template("homepage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            return render_login(mode="login", error="Please enter both user name and password.")

        # TODO: Replace this with database password verification.
        session["user"] = {"name": username, "auth_type": "password"}
        return redirect(url_for("homepage"))

    mode = request.args.get("mode", "login")
    error = request.args.get("error", "")
    success = request.args.get("success", "")
    return render_login(mode=mode, error=error, success=success)


@app.route("/signup", methods=["POST"])
def signup():
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    confirm_password = request.form.get("confirm_password", "").strip()

    if not full_name or not email or not password or not confirm_password:
        return render_login(mode="signup", error="Please fill all sign up fields.")

    if password != confirm_password:
        return render_login(mode="signup", error="Password and confirm password must match.")

    # TODO: Replace this with database user creation.
    return render_login(mode="login", success="Sign up successful. Please sign in.")


@app.route("/auth/google")
def google_auth():
    flow = request.args.get("flow", "login")
    if flow not in {"login", "signup"}:
        flow = "login"
    session["auth_flow"] = flow

    if not app.config["GOOGLE_CLIENT_ID"] or not app.config["GOOGLE_CLIENT_SECRET"]:
        return render_login(
            mode=flow,
            error="Google OAuth is not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.",
        )

    redirect_uri = url_for("google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route("/auth/google/callback")
def google_callback():
    flow = session.pop("auth_flow", "login")
    try:
        token = oauth.google.authorize_access_token()
    except Exception:
        return render_login(mode=flow, error="Google authentication failed. Please try again.")

    user_info = token.get("userinfo")
    if not user_info:
        try:
            user_info = oauth.google.parse_id_token(token)
        except Exception:
            user_info = None

    if not user_info:
        return render_login(mode=flow, error="Unable to read Google profile information.")

    # TODO: Lookup/create user in your database here.
    session["user"] = {
        "name": user_info.get("name") or user_info.get("email", "User"),
        "email": user_info.get("email", ""),
        "auth_type": "google",
    }

    if flow == "signup":
        return render_login(mode="login", success="Google sign up successful. You can continue now.")

    return redirect(url_for("home"))


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/home", methods=['GET'])
def home():
    return "You are in the landing home page"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
