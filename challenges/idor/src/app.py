from flask import Flask, render_template, request

app = Flask(__name__)

# Dummy data representing user profiles
user_profiles = [
    {'id': 1, 'name': 'Admin', 'email': 'flag{y0u_kn0w_about_id0r}'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
    {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'}
]

@app.route('/')
def index():
    return render_template('index.html', profiles=user_profiles)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    # Vulnerable code: directly accessing user profiles based on the provided user_id
    user = user_profiles[user_id - 1]
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True,port=3000)
