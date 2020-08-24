from app import app
from flask import render_template, url_for, flash, redirect, request
from werkzeug.utils import secure_filename
from app.forms import RandomClusterForm, CustomClusterForm
import numpy as np
from app.clustering import Cluster
import os
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/custom', methods=['GET', 'POST'])
def custom():
    formClust = CustomClusterForm()
    # This is a bit weird, combining the request with form class
    if request.method == 'POST' and formClust.validate_on_submit():
        file = request.files["file"]
        if file.filename:
            ext = file.filename.split(".")[1].upper()
            if ext in app.config["ALLOWED_FILE_EXTENSIONS"]:
                filename = secure_filename(file.filename)
                # Delete file with same name in directory
                if os.path.exists(app.config["UPLOAD_FOLDER"]+filename):
                    os.remove(app.config["UPLOAD_FOLDER"]+filename)
                # Save the new file
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                filepath = app.config["UPLOAD_FOLDER"] + filename
                # Get other form data
                ncluster = formClust.numclusters.data
                maxiter = formClust.maxiter.data
                timenow = datetime.now()
                # Apply K-means
                try:
                    Cluster.cluster_csv(filepath, ncluster, maxiter, timenow)
                except Exception as err:
                    flash(f"Something went wrong in the data processing :(. Err: {err}")
                    return render_template("custom.html",form=formClust)
                imgs = sorted(os.listdir(app.config['IMAGE_FOLDER']))
                return render_template("custom.html", form=formClust, imgs=imgs)
            else:
                flash("Please enter a csv file format only.")
        else:
            flash("Please enter a csv file.")
    return render_template('custom.html', form=formClust)


@app.route('/random', methods=['GET', 'POST'])
def random():
    formClust = RandomClusterForm()
    if formClust.validate_on_submit():
        flash("You have successfully submitted your cluster request with {} number of points, {} clusters and {} max "
              "iteration."
              .format(formClust.numpoints.data, formClust.numclusters.data, formClust.maxiter.data))
        # Set up clustering
        ncluster = formClust.numclusters.data
        centroids = np.random.uniform(0, 10, 2*ncluster).reshape((ncluster, 2))
        maxiter = formClust.maxiter.data
        # For data generation, create fake centers
        simcenter = np.random.uniform(0, 10, 2*ncluster).reshape((ncluster, 2))
        # For each fake center generate floor(numpoints/ncluster), except for last one
        numpoints = formClust.numpoints.data
        size = np.floor(numpoints / ncluster)
        for i in range(ncluster):
            if i == ncluster - 1:  # if this is the last iteration give the rest of the points to it
                size = numpoints - (ncluster - 1)*size
            # The center has ~ N(x,1) for the x-axis and ~ N(y,1) for the y-axis
            Xx = np.random.normal(simcenter[i, 0], 1, int(size))
            Yy = np.random.normal(simcenter[i, 1], 1, int(size))
            # Stack horizontally (side by side) and then vertically
            if i == 0:
                X = np.transpose(np.vstack((Xx, Yy)))
            else:
                X = np.vstack((X, np.transpose(np.vstack((Xx, Yy)))))
        timenow = datetime.now()
        Cluster.kmeans(X, centroids, ncluster, maxiter, timenow)
        imgs = sorted(os.listdir(app.config['IMAGE_FOLDER']))
        return render_template('random.html', form=formClust, imgs=imgs)
    return render_template('random.html', form=formClust, imgs=[])


# @app.route('/upload', methods=['GET','POST'])
# def upload():
#     flash("SOMETHING")
#     flash(request.method)
#     flash(str(request.files) + "are the files")
#     if request.method == 'POST':
#         if request.files:
#             file = request.files["file"]
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
#         else:
#             flash("NO")
#     return render_template("upload.html")


