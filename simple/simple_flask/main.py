from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """
    This root route.
    """
    template_name = 'simple_flask'
    return render_template('index.html.j2', template_name=template_name)

if __name__ == "__main__":
    app.run()