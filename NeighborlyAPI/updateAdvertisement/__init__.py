import azure.functions as func

import unit_of_work


def main(req: func.HttpRequest) -> func.HttpResponse:

    id = req.params.get("id")
    request = req.get_json()

    if request:
        try:
            uow = unit_of_work.MongoUnitOfWork()
            collection_name = "advertisements"
            rec_id1 = uow.update_by_id(collection_name, id, request)

            return func.HttpResponse(status_code=200)
        except:
            print("could not connect to mongodb")
            return func.HttpResponse("Could not connect to mongodb", status_code=500)
    else:
        return func.HttpResponse("Please pass name in the body", status_code=400)
