from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def base():
    person = ""
    if request.method == 'POST':
        if request.form['name']:
            person = request.form['name']
    template = '''
        <!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">
            </head>
          <body>
            <form action="" method="post">
              First name:<br>
              <input type="text" name="name" value="">
              <input type="submit" value="Submit">
            </form>
            <h2>Hello %s!</h2>
          </body>
        </html>
    '''% (person)
    return render_template_string(template)

if __name__ == "__main__":
    app.run(debug=True, port=9000)
