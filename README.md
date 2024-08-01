---
page_type: sample
description: "A minimal sample app that can be used to demonstrate deploying FastAPI apps to Azure App Service."
languages:
  - python
products:
  - azure
  - azure-app-service
---

# Deploy a Python (FastAPI) web app to Azure App Service - Sample Application

This is the sample FastAPI application for the Azure Quickstart [Deploy a Python (Django, Flask or FastAPI) web app to Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python). For instructions on how to create the Azure resources and deploy the application to Azure, refer to the Quickstart article.

Sample applications are available for the other frameworks here:

- Django [https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart)
- Flask [https://github.com/Azure-Samples/msdocs-python-flask-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-flask-webapp-quickstart)

If you need an Azure account, you can [create one for free](https://azure.microsoft.com/en-us/free/).

## Local Testing

To try the application on your local machine:

### Install the requirements

`pip install -r requirements.txt`

### Start the application

`uvicorn main:app --reload`

### Example call

http://127.0.0.1:8000/

## Next Steps

To learn more about FastAPI, see [FastAPI](https://fastapi.tiangolo.com/).

## Deploying to Azure

> Following [these](https://learn.microsoft.com/en-us/azure/developer/python/tutorial-containerize-simple-web-app-for-app-service?tabs=web-app-fastapi#create-a-resource-group-and-azure-container-registry) steps

- Pre-requisites
  - Install Azure CLI
  - Install Docker
  - Make sure you are logged in to Azure CLI
    ```
    az login
    ```
- Creating a group
  ```
  az group create --name ai-services --location westus
  ```
- Creating a Container Registry
  ```
  az acr create --resource-group ai-services --name aiservicesacr --sku Basic --admin-enabled true
  ```
- Create ACR password and set it in the environment variable
  ```
  ACR_PASSWORD=$(az acr credential show \
  --resource-group ai-services \
  --name aiservicesacr \
  --query "passwords[?name == 'password'].value" \
  --output tsv)
  ```
- Build the image in Azure Container Registry
  ```
  az acr build --resource-group ai-services --registry aiservicesacr --image fastapi-demo:latest .
  ```
- Create App Service Plan
  ```
  az appservice plan create --name ai-app-services-plan --resource-group ai-services --sku B1 --is-linux
  ```
- Create Web App

  ```
  az webapp create \
  --resource-group ai-services \
  --plan ai-app-services-plan \
  --name bm-fastapi-demo \
  --container-registry-password $ACR_PASSWORD \
  --container-registry-user aiservicesacr \
  --deployment-container-image-name aiservicesacr.azurecr.io/fastapi-demo:latest
  ```

  The `--name` must be unique across Azure.

- Test API

````
curl -X POST bm-fastapi-demo.azurewebsites.net/hindi \
   -H "Content-Type: application/json" \
   -d '{"q": "describe India"}'
   ```
````
