# HAIKUr

This is a haiku-blogging app. You can view it live at [http://haikur.com]


## Running HAIKUr

Running HAIKUr requires Python 2.7, a Google account registered with Google Developer Console, and the Google Cloud SDK. Here are the steps:

+ Sign up at [Google Developer Console](https://console.developers.google.com/) and create a project + Download[Google Cloud SDK](https://cloud.google.com/sdk/docs/) and take the step to set up command line tools as outlined in the instructions
+ Install Jinja2, which is available through pip using ```pip install jinja2```.

### Starting the local development server
+ Clone this repository
+ From the root haikur folder, run ```dev_appserver.py .```
+ View HAIKUr at ```http::/localhost:8080```

### Deploying to Google App Engine
+ ```gcloud app deploy```
+ ```gcloud app browse
