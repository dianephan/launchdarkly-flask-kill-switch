from flask import Flask, render_template, request
import os
import requests
import ldclient
from ldclient.config import Config
import os

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()

sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")

@app.route('/')
def index():
    context = ldclient.Context.builder("context-key-123abc").name("Tetra").build()
    use_cats_api = ldclient.get().variation("use-cats-api", context, False)

    if use_cats_api:
        url = 'https://api.thecatapi.com/v1/images/search'
        response = requests.get(url)
        cat_data = response.json()
        cat_image_url = cat_data[0]['url']
    else:
        cat_image_url = "https://media.tenor.com/ocYNcAWYyHMAAAAM/99-cat.gif"
    return render_template('index.html', cat_image=cat_image_url)

if __name__ == "__main__":
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))

    if not ldclient.get().is_initialized():
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

    print("*** SDK successfully initialized")

    context = \
        ldclient.Context.builder('example-user-key').kind('user').name('Sandy').build()
    
    app.run(debug=True)