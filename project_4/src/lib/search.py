from spacey.en import English
import redis
import pickle

from argparse import ArgumentParser



arg_parser = argparse.ArgumentParser("Search for Wikipedia articles.")

arg_parser.add_argument('-q', '--query', nargs='?', default='meditation',
                        help="search term(s)")

arg_parser.add_argument('-a', '--host', nargs='?', default='localhost',
                        help="app host address")
arg_parser.add_argument('-p', '--port', nargs='?', default=5000, type=int,
                        help="app host port")

arg_parser.add_argument('-m', '--mongo', nargs='?', default='localhost',
                        help="Mongo host address")
arg_parser.add_argument('--mongo-port', nargs='?', default=27017, type=int,
                        help="Mongo host port")

arg_parser.add_argument('-r', '--redis', nargs='?', default='localhost',
                        help="Redis host address")
arg_parser.add_argument('--redis-port', nargs='?', default=6379, type=int,
                        help="Redis host port")
arg_parser.add_argument('--redis-db', nargs='?', default=0, type=int,
                        help="Redis database ID")

arg_parser.add_argument('--model-key', nargs='?', default='n_neighbors.p',
                        help="key to retrieve pickled model from Redis")

args = arg_parser.parse_args()



def search_titles(query, en_pipe, rd_conn, model_key):
    redis_pipe = redis.pipeline()
    query_vector = en_pipe(query).vector.reshape(1,-1)
    n_neigbors = pickle.loads(redis.get(model_key))
    _, indices = n_neigbors.kneighbors(query_vector)
    del n_neigbors
    for index in indices[0]:
        redis_pipe.get(bytes(str(index), encoding='utf-8'))
    return redis_pipe.execute()



en_pipe = English()
rd_conn = redis.StrictRedis(args.redis, args.redis_port, args.redis_db)

print(search_titles(args.query, en_pipe, rd_conn, args.model_key))

