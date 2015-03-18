# coding: utf8
import json
import pymongo
import tornado
import tornado.web
import tornado.ioloop

from tornado.web import RequestHandler

prefix = "api"


def cur2str(cur):
    return json.dumps([dict((k, r[k])
                            for k in r if k not in ["_id"])
                                for r in cur], indent=4)


class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.application.db


class UnitHandler(BaseHandler):

    collect = "users"

    def get(self):
        args = self.request.arguments.items()
        if args:
            query = dict((k, v[0]) for k, v in args if v)
            cur = self.db[self.collect].find(query)
            s = cur2str(cur)
            self.set_header("Content-Type", "application/json")
            self.write(s)

    def post(self):
        body = self.request.body

        if body:
            data = json.loads(body)
            self.db[self.collect].insert(data)
            self.set_header("Content-Type", "application/json")
            self.write("Inserted new user")

    def patch(self):
        args = self.request.arguments.items()
        if args:
            query = {}
            data = {}
            for k, v in args:
                if k == "query":
                    qk, qv = v[0].split("=")
                    query[qk] = qv
                else:
                    data[k] = v[0]

            self.db[self.collect].update(query, {"$set": data})

    def delete(self):
        args = self.request.arguments.items()
        query = dict((i.split("=")) for i in args if i == "query")
        self.db[self.collect].remove(query)


class EchoHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("CRUD test server")


class Application(tornado.web.Application):

    def __init__(self, db):
        handlers = [
            (r'/' + prefix + "/user", UnitHandler),
            (r"/echo", EchoHandler)
        ]

        settings = dict(debug=True)

        tornado.web.Application.__init__(self, handlers, **settings)

        self.conn = pymongo.MongoClient()
        self.db = self.conn[db]


def run():
    app = Application("test")
    app.listen(9005)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
