import flask
from flask import Flask, jsonify, url_for

app = Flask(__name__)  #

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/todo/api/v1.0/tasks', methods=['GET'])  # 装饰器
def get_tasks():
    return jsonify({'tasks': tasks})



@app.route('/')
def index():pass


@app.route('/login')
def login():pass


@app.route('/user/<username>')
def profile(username): pass


if __name__ == '__main__':  # 确保该脚本只有在被python解释器执行的时候才被运行；
    app.run(debug=True)

    # with app.test_request_context():
    print(url_for('login'))
    print(url_for('index'))
    print(url_for('login' ,next='/'))
    print(url_for('profile', username='John Doe'))
