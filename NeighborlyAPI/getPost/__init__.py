import azure.functions as func
from bson.json_util import dumps

import unit_of_work


def main(req: func.HttpRequest) -> func.HttpResponse:

    id = req.params.get("id")

    if id:
        try:
            uow = unit_of_work.MongoUnitOfWork()
            collection_name = "posts"
            result = uow.get_one(collection_name, id)
            result = dumps(result)

            return func.HttpResponse(
                result, mimetype="application/json", charset="utf-8"
            )
        except:
            return func.HttpResponse("Database connection error.", status_code=500)

    else:
        return func.HttpResponse(
            "Please pass an id parameter in the query string.", status_code=400
        )
