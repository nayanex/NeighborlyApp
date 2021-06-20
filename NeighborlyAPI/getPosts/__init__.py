import logging

import azure.functions as func
from bson.json_util import dumps

import unit_of_work


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Python getPosts trigger function processed a request.")

    try:
        uow = unit_of_work.MongoUnitOfWork()
        collection = uow.get_all("posts")
        result = dumps(collection)

        return func.HttpResponse(
            result, mimetype="application/json", charset="utf-8", status_code=200
        )
    except:
        return func.HttpResponse("Bad request.", status_code=400)
