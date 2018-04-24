from flask import Flask
from redis import StrictRedis
from pymongo import MongoClient


app = Flask(__name__)
redis = StrictRedis(host='redis', port=6379)
mongo = MongoClient(host='mongo', port=27017)


@app.route('/')
def hello():
    redis.incr('hits')
    return 'Hello World! I have been seen %s times.\n'.format(redis.get('hits'))


@app.route('/foo')
def hello_foo():
    redis.incr('foo_hits')
    return 'I pity the foo {}\n.'.format(str('!' * int(redis.get('foo_hits'))))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

