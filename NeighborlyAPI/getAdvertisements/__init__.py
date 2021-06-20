import azure.functions as func
from bson.json_util import dumps

import unit_of_work


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        uow = unit_of_work.MongoUnitOfWork()
        collection = uow.get_all("advertisements")

        result = dumps(collection)

        return func.HttpResponse(result, mimetype="application/json", charset="utf-8")
    except:
        print("could not connect to mongodb")
        return func.HttpResponse("could not connect to mongodb", status_code=400)
