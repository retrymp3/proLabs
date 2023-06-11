
from flask import Flask, request, render_template
from lxml import etree

app = Flask(__name__)
app.config['DEBUG'] = True

USERNAME = 'admin' 
PASSWORD = 'admin' 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/doLogin", methods=['POST', 'GET'])
def doLogin():
    result = None
    try:
        tree = etree.fromstring(request.data)
        for childa in tree:
            print(childa.tag, childa.text, childa.attrib)
            if childa.tag == "username":
                username = childa.text
                print(username)
            if childa.tag == "password":
                password = childa.text
                print(password)
        if username == USERNAME and password == PASSWORD:
            result = "<result><code>%d</code><msg>%s</msg></result>" % (1,username)
        else:
            result = "<result><code>%d</code><msg>%s</msg></result>" % (0,username)
    except Exception as Ex:
        result = "<result><code>%d</code><msg>%s</msg></result>" % (3,str(Ex))
    return result,{'Content-Type': 'text/xml;charset=UTF-8'}

def prn_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))


if __name__ == "__main__":
    app.run(debug="True",port=8000)