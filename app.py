from flask import Flask, render_template, request, redirect, url_for

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard/<name>')
    def dashboard(name):
        return render_template('dashboard.html', name=name)


    return app

if __name__ == '__main__':
    create_app().run(debug=True,port=5000,host='0.0.0.0')
