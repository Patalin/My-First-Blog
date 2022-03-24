from flask import Flask, render_template, request
import requests
import smtplib

posts = requests.get("https://api.npoint.io/c98885794f4eb306386f").json()
img_url = "http://wallpapercave.com/wp/OR88Ll1.jpg"

MY_EMAIL = "your_email@example.com"
MY_PASS = 'your_password'


app = Flask(__name__)


@app.route('/')
def get_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods=['GET', 'POST'])
def receive_data():
    if request.method == "POST":
        name = request.form['username']
        email = request.form['user_email']
        phone = request.form['user_phone']
        message = request.form['user_message']

        subject_email = f'Subject:New Message Alert\n\nName: {name}\n\n Email: {email}\n\n Phone: {phone}\n\n Message: {message}'

        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASS)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=email, msg=subject_email)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


if __name__ == "__main__":
    app.run(debug=True)
