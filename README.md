# Deploying the Neighborly App with Azure Functions

## Project Overview

For the final project, we are going to build an app called "Neighborly". Neighborly is a Python Flask-powered web application that allows neighbors to post advertisements for services and products they can offer.

The Neighborly project is comprised of a front-end application that is built with the Python Flask micro framework. The application allows the user to view, create, edit, and delete the community advertisements.

The application makes direct requests to the back-end API endpoints. These are endpoints that we will also build for the server-side of the application.

You can see an example of the deployed app below.

![Deployed App](images/final-app.png)

## Dependencies

You will need to install the following locally:

- [Pipenv](https://pypi.org/project/pipenv/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

On Mac, you can do this with:

```bash
# install pipenv
brew install pipenv

# install azure-cli
brew update && brew install azure-cli

# install azure function core tools 
brew tap azure/functions
brew install azure-functions-core-tools@3
```

## Project Instructions

In case you need to return to the project later on, it is suggested to store any commands you use so you can re-create your work. You should also take a look at the project rubric to be aware of any places you may need to take screenshots as proof of your work (or else keep your resource up and running until you have passed, which may incur costs).

### I. Creating Azure Function App

We need to set up the Azure resource group, region, storage account, and an app name before we can publish.

1. Create a resource group.
2. Create a storage account (within the previously created resource group and region).
3. Create an Azure Function App within the resource group, region and storage account. 
   - Note that app names need to be unique across all of Azure.
   - Make sure it is a Linux app, with a Python runtime.

    Example of successful output, if creating the app `myneighborlyapiv1`:

    ```bash
    Your Linux function app 'myneighborlyapiv1', that uses a consumption plan has been successfully created but is not active until content is published using Azure Portal or the Functions Core Tools.
    ```

4. Set up a Cosmos DB Account. You will need to use the same resource group, region and storage account, but can name the Cosmos DB account as you prefer. **Note:** This step may take a little while to complete (15-20 minutes in some cases).

5. Create a MongoDB Database in CosmosDB Azure and two collections, one for `advertisements` and one for `posts`.
6. Print out your connection string or get it from the Azure Portal. Copy/paste the **primary connection** string.  You will use it later in your application.

    Example connection string output:
    ```bash
    bash-3.2$ Listing connection strings from COSMOS_ACCOUNT:
    + az cosmosdb keys list -n neighborlycosmos -g neighborlyapp --type connection-strings
    {
    "connectionStrings": [
        {
        "connectionString": "AccountEndpoint=https://neighborlycosmos.documents.azure.com:443/;AccountKey=xxxxxxxxxxxx;",
        "description": "Primary SQL Connection String"
        },
        {
        "connectionString": "AccountEndpoint=https://neighborlycosmos.documents.azure.com:443/;AccountKey=xxxxxxxxxxxxx;",
        "description": "Secondary SQL Connection String"
        } 
        
        ... [other code omitted]
    ]
    }
    ```

7. Import Sample Data Into MongoDB.
   - Download dependencies:
        ```bash
        # get the mongodb library
        brew install mongodb-community@4.2

        # check if mongoimport lib exists
        mongoimport --version
        ```

    - Import the data from the `sample_data` directory for Ads and Posts to initially fill your app.

        Example successful import:
        ```
        Importing ads data ------------------->
        2020-05-18T23:30:39.018-0400  connected to: mongodb://neighborlyapp.mongo.cosmos.azure.com:10255/
        2020-05-18T23:30:40.344-0400  5 document(s) imported successfully. 0 document(s) failed to import.
        ...
        Importing posts data ------------------->
        2020-05-18T23:30:40.933-0400  connected to: mongodb://neighborlyapp.mongo.cosmos.azure.com:10255/
        2020-05-18T23:30:42.260-0400  4 document(s) imported successfully. 0 document(s) failed to import.
        ```

8. Hook up your connection string into the NeighborlyAPI server folder. You will need to replace the *url* variable with your own connection string you copy-and-pasted in the last step, along with some additional information.
    - Tip: Check out [this post](https://docs.microsoft.com/en-us/azure/cosmos-db/connect-mongodb-account) if you need help with what information is needed.
    - Go to each of the `__init__.py` files in getPosts, getPost, getAdvertisements, getAdvertisement, deleteAdvertisement, updateAdvertisement, createAdvertisements and replace your connection string. You will also need to set the related `database` and `collection` appropriately.

    ```bash
    # inside getAdvertisements/__init__.py

    def main(req: func.HttpRequest) -> func.HttpResponse:
        logging.info('Python getAdvertisements trigger function processed a request.')

        try:
            # copy/paste your primary connection url here
            #-------------------------------------------
            url = ""
            #--------------------------------------------

            client=pymongo.MongoClient(url)

            database = None # Feed the correct key for the database name to the client
            collection = None # Feed the correct key for the collection name to the database

            ... [other code omitted]
            
    ```

    Make sure to do the same step for the other 6 HTTP Trigger functions.

9. Deploy your Azure Functions.

    1. Test it out locally first.

        ```bash
        # cd into NeighborlyAPI
        cd NeighborlyAPI

        # install dependencies
        pipenv install

        # go into the shell
        pipenv shell

        # test func locally
        func start
        ```

        You may need to change `"IsEncrypted"` to `false` in `local.settings.json` if this fails.

        At this point, Azure functions are hosted in localhost:7071.  You can use the browser or Postman to see if the GET request works.  For example, go to the browser and type in: 

        ```bash
        # example endpoint for all advertisements
        http://localhost:7071/api/getadvertisements

        #example endpoint for all posts
        http://localhost:7071/api/getposts
        ```

    2. Now you can deploy functions to Azure by publishing your function app.

        The result may give you a live url in this format, or you can check in Azure portal for these as well:

        Expected output if deployed successfully:
        ```bash
        Functions in <APP_NAME>:
            createAdvertisement - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/createadvertisement

            deleteAdvertisement - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/deleteadvertisement

            getAdvertisement - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/getadvertisement

            getAdvertisements - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/getadvertisements

            getPost - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/getpost

            getPosts - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/getposts

            updateAdvertisement - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/updateadvertisement

        ```

        **Note:** It may take a minute or two for the endpoints to get up and running if you visit the URLs.

        Save the function app url **https://<APP_NAME>.azurewebsites.net/api/** since you will need to update that in the client-side of the application.

### II. Deploying the client-side Flask web application

We are going to update the Client-side `settings.py` with published API endpoints. First navigate to the `settings.py` file in the NeighborlyFrontEnd/ directory.

Use a text editor to update the API_URL to your published url from the last step.
```bash
# Inside file settings.py

# ------- For Local Testing -------
#API_URL = "http://localhost:7071/api"

# ------- For production -------
# where APP_NAME is your Azure Function App name 
API_URL="https://<APP_NAME>.azurewebsites.net/api"
```

### III. CI/CD Deployment

1. Deploy your client app. **Note:** Use a **different** app name here to deploy the front-end, or else you will erase your API. From within the `NeighborlyFrontEnd` directory:
    - Install dependencies with `pipenv install`
    - Go into the pip env shell with `pipenv shell`
    - Deploy your application to the app service. **Note:** It may take a minute or two for the front-end to get up and running if you visit the related URL.

    Make sure to also provide any necessary information in `settings.py` to move from localhost to your deployment.

2. Create an Azure Registry and dockerize your Azure Functions. Then, push the container to the Azure Container Registry.
3. Create a Kubernetes cluster, and verify your connection to it with `kubectl get nodes`.
4. Deploy app to Kubernetes, and check your deployment with `kubectl config get-contexts`.

### IV. Event Hubs and Logic App

1. Create a Logic App that watches for an HTTP trigger. When the HTTP request is triggered, send yourself an email notification.
2. Create a namespace for event hub in the portal. You should be able to obtain the namespace URL.
3. Add the connection string of the event hub to the Azure Function.

### V.  Cleaning Up Your Services

Before completing this step, make sure to have taken all necessary screenshots for the project! Check the rubric in the classroom to confirm.

Clean up and remove all services, or else you will incur charges.

```bash
# replace with your resource group
RESOURCE_GROUP="<YOUR-RESOURCE-GROUP>"
# run this command
az group delete --name $RESOURCE_GROUP
```

## Steps I Took

If you could not retrieve your `local.settings.json`, but still have the createAdvertisement deleteAdvertisement code and so on, you can create a fresh Azure Function app. You can run the following shell scripts to create a new Function App.

First we create our storage account. We use the following command:

### Part 1 - Azure Function App

```
STORAGE_ACCT_NAME=neighborly4pp5torage
RESOURCE_GROUP=neighborly-app-rg
REGION=westeurope

az storage account create \
 --name $STORAGE_ACCT_NAME \
 --resource-group $RESOURCE_GROUP \
 --location $REGION
```

```
#!/bin/bash

# must be a unique, you can obtain these in the Azure Portal
STORAGE_ACCT_NAME=neighborly4pp5torage
FUNCTION_APP_NAME=neighborly-function-app
RESOURCE_GROUP=neighborly-app-rg
REGION=westeurope

# Create Your Function App
az functionapp create \
    --name $FUNCTION_APP_NAME \
    --storage-account $STORAGE_ACCT_NAME \
    --resource-group $RESOURCE_GROUP \
    --os-type Linux \
    --consumption-plan-location $REGION \
    --runtime python
```

### Deploying with Azure CLI

The command for deploying your functions in Azure CLI is:

Make sure you also install:

`pipenv install azure-cli-core`

```
func azure functionapp publish $FUNCTION_APP_NAME --python
```

If Azure cannot find your function, make sure you are in the correctly directory and that your `local.settings.json` is current.


### how to sync local.setting.json in VS and Azure

You can sync settings between local and Azure with Func CLI:

```
func azure functionapp fetch-app-settings $FUNCTION_APP_NAME # to copy from Azure to local
func azure functionapp publish $FUNCTION_APP_NAME --publish-settings-only # to copy from local to Azure
```

### Resource

[Create a Python function in Azure from the command line](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser)

### Set up a Cosmos DB Account

#### 1. Create a new CosmosDB account.

```
# This is the new account here
COSMOSDB_ACCT=neighborly0cosmos4cct

az cosmosdb create -n $COSMOSDB_ACCT -g $RESOURCE_GROUP  \
    --locations regionName=$REGION failoverPriority=0 isZoneRedundant=False \
    --kind "MongoDB"
```

Note: It may take a while for the CosmosDB account to be created, sometimes on the order of 10-20 minutes.

#### 2. Creating a new MongoDB database with a sample collection

```
DB_NAME=neighborly-db
CREATE_LEASE_COLLECTION=0     # yes,no=(1,0)

# Get your CosmosDB key and save as a variable
COSMOSDB_KEY=$(az cosmosdb keys list --name $COSMOSDB_ACCT --resource-group $RESOURCE_GROUP --output tsv |awk '{print $1}')

az cosmosdb database create \
    --name $COSMOSDB_ACCT \
    --db-name $DB_NAME \
    --key $COSMOSDB_KEY \
    --resource-group $RESOURCE_GROUP
    
SAMPLE_COLLECTION_ADS=advertisements
SAMPLE_COLLECTION_POSTS=posts

# Create a container with a partition key and provision 400 RU/s throughput.
az cosmosdb mongodb collection create \
    --resource-group $RESOURCE_GROUP \
    --name $SAMPLE_COLLECTION_ADS \
    --account-name $COSMOSDB_ACCT \
    --database-name $DB_NAME \
    --throughput 400

az cosmosdb mongodb collection create \
    --resource-group $RESOURCE_GROUP \
    --name $SAMPLE_COLLECTION_POSTS \
    --account-name $COSMOSDB_ACCT \
    --database-name $DB_NAME \
    --throughput 400
```

#### 3. Listing connection strings from COSMOS_ACCOUNT:

```
az cosmosdb keys list -n $COSMOSDB_ACCT -g $RESOURCE_GROUP --type connection-strings
```

#### 4. Import Sample Data Into MongoDB.

Download dependencies:

```
# get the mongodb library
brew install mongodb-community@4.2

# check if mongoimport lib exists
mongoimport --version
```

#### 5. Import the data from the sample_data directory for Ads and Posts to initially fill your app.

```
# This information is viewable in your portal >> Azure Cosmos DB >> Select the DB name >> Settings >> Connection String >>
# replace the host, port, username, and primary password with your own

MONGODB_HOST=neighborly0cosmos4cct.mongo.cosmos.azure.com
MONGODB_PORT=10255
USER=neighborly0cosmos4cct

# Copy/past the primary password here
PRIMARY_PW=0CqJu57Vwe18E4gC7IX8TLCT2enJ4olAnaeqjhzRFyAgHdra0xUnOvGz3r1IbwVRq0M4q8Ye8UNLirOxCybaZw==

FILE_DIR_ADS=../sample_data/sampleAds.json
FILE_DIR_POSTS=../sample_data/samplePosts.json

#Import command for Linux and Mac OS

mongoimport -h $MONGODB_HOST:$MONGODB_PORT \
-d $DB_NAME -c $SAMPLE_COLLECTION_ADS -u $USER -p $PRIMARY_PW \
--ssl  --jsonArray  --file $FILE_DIR_ADS --writeConcern "{w:0}"

mongoimport -h $MONGODB_HOST:$MONGODB_PORT \
-d $DB_NAME -c $SAMPLE_COLLECTION_POSTS -u $USER -p $PRIMARY_PW \
--ssl  --jsonArray  --file $FILE_DIR_ADS --writeConcern "{w:0}"

```

### Part2 - Deploy your client app.

Make sure `Werkzeug<1.0` because `werkzeug.contrib.atom` is deprecated in recent versions of `Werkzeug`

Also the code does not use `dominate`, `visitor`, `azure-functions`, `flask-restplus` and `flask_swagger_ui` for anything. You can remove  them.

You can deploy the client-side Flask app with:

```
APP_NAME=neighborly-webapp
RESOURCE_GROUP=neighborly-app-rg
REGION=westeurope

az webapp up \
 --resource-group $RESOURCE_GROUP \
 --name $APP_NAME \
 --sku F1 \
 --location $REGION\
 --verbose
```

After running this command once, a configuration file will be created that will store any arguments you gave the previous time, so you can run just `az webapp up` and it will re-use arguments. Note that certain updates, such as changes to requirements.txt files, won't be appropriately pushed just by using `az webapp up`, so you may need to use az webapp update or just delete the app and re-deploy.

```
az webapp up \
 --name $APP_NAME \
 --verbose 
```

Once deployed, the flask app will be available at the URL `http://<APP_NAME>.azurewebsites.net/` - meaning the app name you use must be unique.

### Part 3: CI/CD Deployment

1. Create an Azure Registry 
2. Dockerize your Azure Functions

#### Deploying a function app to Kubernetes

> You can deploy any function app to a Kubernetes cluster running KEDA. Since your functions run in a Docker container, your project needs a Dockerfile. If it doesn't already have one, you can add a Dockerfile by running the following command at the root of your Functions project:

`func init --docker-only`

> The Core Tools will leverage the docker CLI to build and publish the image. Be sure to have docker installed already and connected to your account with docker login.

```
REGISTRY_SERVER=neighborlyregistry.azurecr.io
REGISTRY=neighborlyRegistry
docker login $REGISTRY_SERVER
```

> To create an image from Docker file use the below commands, in which we also tag our image

```
TAG=neighborlyregistry.azurecr.io/neighborly-api:v1
docker build -t $TAG .

# List your images with:
docker images
```

3. push the container to the Azure Container Registry

```
REGISTRY_SERVER=neighborlyregistry.azurecr.io

az acr login --name $REGISTRY_SERVER
docker push <your-registry-name>.azurecr.io/<your-image-name>

# other useful commands
az acr show --name $REGISTRY --query loginServer --output table
az acr repository list --name $REGISTRY_SERVER --output table
```

4. Create a Kubernetes cluster, and verify your connection to it with `kubectl get nodes`

> Install kubectl in MacOS

* Run the installation command: `brew install kubectl orbrew install kubernetes-cli`
* Test to ensure the version you installed is up-to-date: `kubectl version --client`

> Create AKS Cluster. Note: Kubernetes name must match ^[a-z0-9\-\.]*$.

```
RESOURCE_GROUP=neighborly-app-rg
AKS_CLUSTER=neighborly-aks-cluster

az aks create --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER --node-count 2 --enable-addons monitoring --generate-ssh-keys

# Merge "neighborly-aks-cluster" as current context in /Users/<username>/.kube/config
az aks get-credentials --name $AKS_CLUSTER --resource-group $RESOURCE_GROUP

#verify your connection to it with:
kubectl get nodes
```

5. Deploy app to Kubernetes, and check your deployment with `kubectl config get-contexts`.

> To run Functions on your Kubernetes cluster, you must install the KEDA component. You can install this component using Azure Functions Core Tools.
```
func kubernetes install --namespace keda
```

```
RESOURCE_GROUP=neighborly-app-rg
AKS_CLUSTER=neighborly-aks-cluster
IMAGE_NAME=neighborlyregistry.azurecr.io/neighborly-api:v1
REGISTRY=neighborlyRegistry

# Update a managed Kubernetes cluster. Where --attach-acr grants the 'acrpull' role assignment to the ACR specified by name or resource ID. It might take up to 10 minutes or more for it to work. be patient.
az aks update -n $AKS_CLUSTER -g $RESOURCE_GROUP --attach-acr $REGISTRY 

func kubernetes deploy --name $AKS_CLUSTER \
--image-name $IMAGE_NAME \
-—polling-interval 3 —cooldown-period 5
```

> Troubleshooting deployment errors

```
https://knowledge.udacity.com/questions/546910

REGISTRY_SERVER=neighborlyregistry.azurecr.io

az aks check-acr -n $AKS_CLUSTER -g $RESOURCE_GROUP \
--acr $REGISTRY_SERVER

```

#### These are other useful docker commands:

```
# Remove <none> images: 
rmi $(docker images -f "dangling=true" -q)

# List containers:
docker container ls [OPTIONS]

# [docker stop]: Stop one or more running containers
docker stop [OPTIONS] CONTAINER [CONTAINER...]

# [docker rm]: Remove one or more containers
docker rm [OPTIONS] CONTAINER [CONTAINER...]

# [docker image rm]: Remove one or more images
docker image rm [OPTIONS] IMAGE [IMAGE...]

# Test an image in your local machine
docker run -p 8080:80 -it $IMAGE_NAME
```

### Part 4: Event Hubs and Logic App

[Azure Event Hubs trigger for Azure](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-event-hubs-trigger?tabs=python)


1. Create a Logic App that watches for an HTTP trigger. When the HTTP request is triggered, send yourself an email notification.

https://docs.microsoft.com/en-us/azure/connectors/connectors-create-api-smtp

2. Create a namespace for event hub in the portal. You should be able to obtain the namespace URL.

[create-an-event-hubs-namespace](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create#create-an-event-hubs-namespace)

3. Add the connection string of the event hub to the Azure Function.

```json
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "type": "eventHubTrigger",
      "name": "event",
      "direction": "in",
      "eventHubName": "neighborly-hub",
      "connection": "EventHubConnString"
    }
  ]
}
```

Your `local.settings.json` should look like this:

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "FUNCTIONS_EXTENSION_VERSION": "~2",
    "AzureWebJobsStorage": "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=neighborly4pp5torage;AccountKey=IuzsjtsibcwXzMnymoEy220fdht7FE/WALywgxATBQ8il044ft9eZhnEele6bkRaPe0wB7j+TMTSsHq082BLKw==",
    "APPINSIGHTS_INSTRUMENTATIONKEY": "be45bd8a-c876-461f-911a-0d3b05546f6d",
    "MongoDBConnString": "mongodb://neighborly0cosmos4cct:0CqJu57Vwe18E4gC7IX8TLCT2enJ4olAnaeqjhzRFyAgHdra0xUnOvGz3r1IbwVRq0M4q8Ye8UNLirOxCybaZw==@neighborly0cosmos4cct.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@neighborly0cosmos4cct@",
    "MongoDBName": "neighborly-db",
    "EventHubConnString": "Endpoint=sb://neighborly-namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=37zZb6Jg/hv2rZ0AUTu6AAgIJU/yYN4L7sl3e+svi60="
  },
  "ConnectionStrings": {}
}
```
### [Route custom events to Azure Event Hubs with Azure CLI and Event Grid](https://docs.microsoft.com/en-us/azure/event-grid/custom-event-to-eventhub)

### Create a Custom Topic

An event grid topic provides a user-defined endpoint that you post your events to. The following example creates the custom topic in your resource group. Replace <your-topic-name> with a unique name for your custom topic. The custom topic name must be unique because it's represented by a DNS entry.

```
TOPICNAME=neighborly-topic
RESOURCE_GROUP=neighborly-app-rg
REGION=westeurope


az eventgrid topic create --name $TOPICNAME -l $REGION -g $RESOURCE_GROUP
```

In the end we are going to have an endpoint generated, like this one, which we will use for our POST request:

```
endpoint": "https://neighborly-topic.westeurope-1.eventgrid.azure.net/api/events
```

#### Create event hub

Before subscribing to the custom topic, let's create the endpoint for the event message. You create an event hub for collecting the events.

```
NAMESPACE=neighborly-namespace
HUBNAME=neighborly-hub
RESOURCE_GROUP=neighborly-app-rg

az eventhubs namespace create --name $NAMESPACE --resource-group $RESOURCE_GROUP

az eventhubs eventhub create --name $HUBNAME --namespace-name $NAMESPACE --resource-group $RESOURCE_GROUP
```

After these commands collect the following:

`serviceBusEndpoint": "https://neighborly-namespace.servicebus.windows.net:443/`
#### Subscribe to a custom topic

You subscribe to an **event grid topic** to tell **Event Grid** which events you want to track. The following example subscribes to the custom topic you created, and passes the resource ID of the **event hub** for the endpoint. The endpoint is in the format:

`/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.EventHub/namespaces/<namespace-name>/eventhubs/<hub-name>`

The following script gets the resource ID for the **event hub**, and subscribes to an **event grid topic**. It sets the endpoint type to **eventhub** and uses the event hub ID for the endpoint.

```
HUBID=$(az eventhubs eventhub show --name $HUBNAME --namespace-name $NAMESPACE --resource-group $RESOURCE_GROUP --query id --output tsv)
TOPICID=$(az eventgrid topic show --name $TOPICNAME -g $RESOURCE_GROUP --query id --output tsv)

az eventgrid event-subscription create \
  --source-resource-id $TOPICID \
  --name subtoeventhub \
  --endpoint-type eventhub \
  --endpoint $HUBID
```
### Send an event to your custom topic

Let's trigger an event to see how Event Grid distributes the message to your endpoint. First, let's get the URL and key for the custom topic.

```
ENDPOINT=$(az eventgrid topic show --name $TOPICNAME -g $RESOURCE_GROUP --query "endpoint" --output tsv)
KEY=$(az eventgrid topic key list --name $TOPICNAME -g $RESOURCE_GROUP --query "key1" --output tsv)
```

In the end you would have something like this, where KEY is our `aeg-sas-key` key to put in the **header** of our POST request:

```
ENDPOINT = https://neighborly-topic.westeurope-1.eventgrid.azure.net/api/events`
KEY = KXCk4H/JZNoXVop3dvzmSuXMfboek1OrPNGju+JVz10=
```

To simplify this article, you use sample event data to send to the custom topic. Typically, an application or Azure service would send the event data. CURL is a utility that sends HTTP requests. In this article, use CURL to send the event to the custom topic. The following example sends three events to the event grid topic:

```
for i in 1 2 3
do
   EVENT='[ {"id": "'"$RANDOM"'", "eventType": "recordInserted", "subject": "myapp/vehicles/motorcycles", "eventTime": "'`date +%Y-%m-%dT%H:%M:%S%z`'", "data":{ "make": "Ducati", "model": "Monster"},"dataVersion": "1.0"} ]'
   curl -X POST -H "aeg-sas-key: $KEY" -d "$EVENT" $ENDPOINT
done
```

#### Using POSTMAN to trigger an EvenHub Event

Your URL should look like this:

`https://neighborly-topic.westeurope-1.eventgrid.azure.net/api/events`

Your body of POST request should look like this:

```json
[
    {
        "id": "1",
        "eventType": "recordInserted",
        "subject": "myapp/vehicles/motorcycles",
        "eventTime": "2020-07-15T21:08:20+00:00",
        "data": {
            "make": "Ducati",
            "model": "Monster"
        },
        "dataVersion": "1.0",
        "metadataVersion": "1",
        "topic": "/subscriptions/bb272072-9c6d-4e28-b814-947814c3e6ef/resourceGroups/neighborly-app-rg/providers/Microsoft.EventGrid/topics/neighborly-topic"
    }
]
```

your **header** should have:

```
key=aeg-sas-key
value=KXCk4H/JZNoXVop3dvzmSuXMfboek1OrPNGju+JVz10=
```


### What is the difference between event hub and event grid? 

https://medium.com/@sreeramg/what-is-microsoft-azure-event-hubs-1ec100452067
https://docs.microsoft.com/en-us/dotnet/api/microsoft.servicebus.messaging.eventdata?view=azure-dotnet
https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-event-hubs
https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-event-hubs-output
https://docs.microsoft.com/en-us/azure/azure-functions/functions-reliable-event-processing

#### Pipenv Useful Commands

```
pipenv shell
pipenv install
pipenv lock --pre --clear

pipenv install sendgrid   
pipenv install isort --dev
pipenv install black --dev

deactivate
exit
pipenv install sendgrid   
pipenv uninstall numpy
pipenv uninstall --all

pipenv lock -r > requirements.txt  
```

##### Prettify your JSON in your web browser

View json in a "prettier" way in Chrome or other web browser with a plugin: `JSON viewer`.


#### Other Resources about Azure Event Hub

https://github.com/yokawasa/azure-functions-python-samples/blob/master/v1functions/eventhub-trigger-table-out-bindings/README.md
https://pypi.org/project/azure-eventhub/#publish-events-to-an-event-hub
https://docs.microsoft.com/en-us/rest/api/eventhub/send-event
https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-python-get-started-send


