import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from numpy import newaxis
from app import app
import os, shutil


# Save to DB instead of file directory -- In fact it is probably better to keep the images in a file system and potentially
# the file names in a DB
class Cluster():
    def cluster_label(x, centroids):
        return np.argmin(np.linalg.norm(x - centroids[:, newaxis, :], axis=2), axis=0)

    def new_centroids(x, label, ncluster):
        new_centroids = np.zeros((ncluster, x.shape[-1]))  # -> want n by p
        for clust in range(ncluster):
            new_centroids[clust,] = np.mean(x[label == clust,], axis=0)
        return new_centroids

    # Assume x is n by 2 (because of 2 graph), and centroids in nclust by 2
    # The additional timenow parameter was added so that it would append to the file image name
    # This was used to fix the image caching prbolem which would lead to seeing the old cluster picture
    def kmeans(x, centroids, ncluster, maxiter, timenow):
        # Clean the contents of the folder
        folder = app.config['IMAGE_FOLDER']
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        # Set the plot limits
        llim = np.floor(x.min())
        ulim = np.ceil(x.max())
        # Initial plots with no colors, just data points and initial cluster centroids
        _, ax = plt.subplots(figsize=(ulim-llim, ulim-llim))
        ax.scatter(x=x[:,0], y=x[:,1], color='black', alpha=0.4, s=40)
        ax.scatter(x=centroids[:,0],y=centroids[:,1], color='black', marker='*', s=95, edgecolor='black')
        ax.set_ylim([llim, ulim])
        ax.set_xlim([llim, ulim])
        ax.set_title('Initial cluster centroids and data points')
        plt.savefig(app.config['IMAGE_FOLDER'] + 'cluster0-{}.png'.format(timenow))
        # assign some random color generation for each cluster
        colors = cm.rainbow(np.linspace(0, 1, ncluster))
        # for the stopping criteria
        prev_centroids = None
        for i in range(maxiter):
            # assign each data point to a cluster
            label = Cluster.cluster_label(x, centroids)
            # plots each cluster and centroid in a color
            _, ax = plt.subplots(figsize=(ulim-llim, ulim-llim))
            ax.scatter(x=x[:,0], y=x[:,1], color=[colors[lab, :] for lab in label], alpha=0.4, s=40)
            ax.scatter(x=centroids[:,0],y=centroids[:,1], color=colors, marker='*', s=95, edgecolor='black')
            ax.set_ylim([llim, ulim])
            ax.set_xlim([llim, ulim])
            ax.set_title('k-means clustering iteration ' + str(i))
            plt.savefig(app.config['IMAGE_FOLDER']+'cluster{}-{}.png'.format(i+1, timenow))
            # find the new centroid for each cluster
            centroids = Cluster.new_centroids(x, label, ncluster)
            # Use difference in centroid to terminate algorithm
            if prev_centroids is not None and np.sum(np.abs(prev_centroids - centroids)) == 0:
                exit_msg = "No new change in the cluster at iteration {}. Will stop iterating.".format(i)
                break
            prev_centroids = centroids

    # Cluster a csv file of 2-dim data
    def cluster_csv(filepath, ncluster, maxiter, timenow):
        try:
            df = pd.read_csv(filepath)
            X = df.to_numpy()
            # For the initial cluster centroids, assign randomly
            centroids = np.random.uniform(X.min(), X.max(), ncluster*2).reshape((ncluster, 2))
            Cluster.kmeans(X, centroids, ncluster, maxiter, timenow)
        except Exception as err:
            raise err


# np.random.seed(22)
# centroids = np.array([[1.5, 2.1],
#                       [2, 1.7],
#                       [2.5, 2.7]])
# X1 = np.random.normal(0, 1, 30).reshape(-1, 2)
# X2 = np.random.normal(3, 1, 30).reshape(-1, 2)
# X3 = np.random.normal(6, 1, 30).reshape(-1, 2)
# X = np.vstack((X1, X2, X3))
# Cluster.kmeans(X, centroids, 3, 15)