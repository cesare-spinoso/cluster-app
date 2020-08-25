# The cluster-app
This application either takes a custom csv input file or produces random data and then clusters it using k-means clustering.

### Requirements

This code requires Python 3.* as well as the Flask library.

### Python Virtual Environment

Create a Python virtual environment called `venv` and install Flask dependencies

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Running the App

Run the application locally with `flask run` setting `FLASK_APP = cluster-app.py`. No database is used as a file system is employed to handle the image processing.

### Deployment
This application is deployed on heroku and can be found [here](https://the-clustering-app.herokuapp.com/index). Please try it out a few times to see different plots. As some of you might know, picking the cluster centroid is crucial for k-means to converge. Some of the plots might come out weird looking but this is because the cluster centroids are picked randomly!

