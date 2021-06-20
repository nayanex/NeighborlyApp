import azure.functions as func
from bson.json_util import dumps

import unit_of_work


def main(req: func.HttpRequest) -> func.HttpResponse:
    # example call http://localhost:7071/api/getAdvertisement/?id=5ec34b2265403b17d00ae864
    id = req.params.get("id")

    if id:
        try:
            uow = unit_of_work.MongoUnitOfWork()
            collection_name = "advertisements"
            result = uow.get_one(collection_name, id)

            print("----------result--------")
            result = dumps(result)
            print(result)

            return func.HttpResponse(
                result, mimetype="application/json", charset="utf-8", status_code=200
            )
        except:
            return func.HttpResponse("Database connection error.", status_code=500)

    else:
        return func.HttpResponse(
            "Please pass an id parameter in the query string.", status_code=400
        )
