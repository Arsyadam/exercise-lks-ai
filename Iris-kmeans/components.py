from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np


def manhattan(x, c):
     return (np.abs(x - c)).sum(axis=2)

def euclidean(x, c):
     return np.sqrt(((x - c) ** 2).sum(axis=2))

def minkowski(x, c, p=1.5):
     return (np.abs(x - c)).sum(axis=2) ** (1/p)

def plotting(X: np.array, labels: np.array, centroids: np.array):
	plt.scatter(X[:, 1], X[:, 2], c=labels)
	plt.scatter(centroids[:, 1], centroids[:, 2], color='red')
	plt.show()
 

class WeightedKmeans:
     
     def __init__(self, n_clusters=3, max_iters=100, distance=euclidean):
          self.n_clusters = n_clusters
          self.max_iters = max_iters
          self.distance = distance
          self._centroids = None
          self._labels = None
          self._epsilon = 1e-9
          
          
     def fit(self, X: np.array):
          centroids = X[np.random.choice(X.shape[0], self.n_clusters, replace=False)]
          
          for iter in range(self.max_iters):
               # assign labels
               labels = self._assign_label(X, centroids)
               
               # update centroids 
               new_centroids = self._update_centroids(X, labels)
               
               # stop convergence
               # if iter % 3 == 0:
               #      # plotting(X, labels, new_centroids, iter)
               #      if np.all(centroids == new_centroids):
               #           print(f'Centroids converged at iter: {iter+1}')
               #           break
               
               centroids = new_centroids
               
          self._centroids = centroids
          self._labels = labels
               
               
     def _assign_label(self, X: np.array, centroids: np.array):
          weights = []
          distances = self.distance(X[:, np.newaxis], centroids)
          for distance in distances:
               weight = [1 / (d + self._epsilon) for d in distance]
               weights.append(weight)
          return np.argmax(weights, axis=1)
     
     
     def _update_centroids(self, X: np.array, labels: np.array):
          new_centroids = np.array([ X[labels == i].mean(axis=0) for i in range(self.n_clusters) ])
          return new_centroids
     
     
     def _inertia(self, X: np.array, labels: np.array):
          inertia = 0
          
          for i in range(self.n_clusters):
               cluster_points = X[labels == i]
               inertia += np.sum((cluster_points - self._centroids[i]) ** 2)
               
          return inertia
     
               
     def _silhouette(self, X: np.array, labels: np.array):

          n_points = len(X)
          unique_labels = np.unique(labels)
          scores = []

          for i in range(n_points):
               current_point = X[i]
               current_label = labels[i]

               # Intra-cluster distance (a)
               same_cluster_indices = np.where(labels == current_label)[0]
               if len(same_cluster_indices) > 1:
                    # Exclude the current point from intra-cluster distance calculation
                    a = np.mean([
                         np.sqrt(((current_point - X[j]) ** 2).sum())
                         for j in same_cluster_indices if j != i
                    ])

               # Nearest-cluster distance (b)
               b = 0
               for other_label in unique_labels:
                    if other_label != current_label:
                         other_cluster_indices = np.where(labels == other_label)[0]
                         mean_distance = np.mean([
                              np.sqrt(((current_point - X[j]) ** 2).sum())
                              for j in other_cluster_indices
                         ])
                         b = min(b, mean_distance)

               # Silhouette score for the current point
               s = (b - a) / max(a, b) if max(a, b) > 0 else 0
               scores.append(s)

          # Return the mean silhouette score for all points
          return np.mean(scores)


class KNN:
	def __init__(self, k=3):
		self.k = k

	def fit(self, X, y):
		self.X_train = X
		self.y_train = y

	def euclidean_distance(self, x1, x2):
		return np.sqrt(np.sum((x1 - x2) ** 2))

	def predict(self, X):
		y_pred = [self._predict(x) for x in X]
		return np.array(y_pred)

	def _predict(self, x):
		distances = [self.euclidean_distance(x, x_train) for x_train in self.X_train]
		k_indices = np.argsort(distances)[:self.k]
		k_nearest_labels = [self.y_train[i] for i in k_indices]
		most_common = np.bincount(k_nearest_labels).argmax()
		return most_common


# def elbow_method_inertia(X, max_k: int, distance_method):
#      scores = []
     
#      for k in range(1, max_k+1):
#           kmeans = WeightedKmeans(n_clusters=k, max_iters=10, distance=distance_method)
#           kmeans.fit(np.array(X))
#           intertia = kmeans._inertia(np.array(X), kmeans._labels)
#           scores.append(intertia)
          
#      plt.plot(range(1, max_k+1), scores, marker='o')
#      plt.xlabel('Number of cluster k')
#      plt.ylabel('inertia score')
#      plt.show()
     
     
def elbow_method_inertia(scores):

     # Create a Matplotlib figure
     fig = Figure(figsize=(5, 4), dpi=100)
     ax = fig.add_subplot(111)
     ax.plot(range(1, 11), scores, marker='o')
     ax.set_xlabel('Number of cluster k')
     ax.set_ylabel('Inertia score')
     ax.set_title('Inertia Scores for Different k')
     
     return fig

def elbow_method_silhoutte(scores):

     # Create a Matplotlib figure
     fig = Figure(figsize=(5, 4), dpi=100)
     ax = fig.add_subplot(111)
     ax.plot(range(1, 11), scores, marker='o')
     ax.set_xlabel('Number of cluster k')
     ax.set_ylabel('Silhouette score')
     ax.set_title('Silhouette Scores for Different k')
     
     return fig

def plotting(X: np.array, labels: np.array, centroids: np.array):
    # Create a Matplotlib figure
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Scatter plot for data points
    ax.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', label="Data Points")
    
    # Scatter plot for centroids
    ax.scatter(centroids[:, 0], centroids[:, 1], color='red', marker='x', s=100, label="Centroids")
    
    # Set plot labels and title
    ax.set_title("Cluster Plot")
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.legend()
    
    return fig
     
     
# # only use top 2 feature with the most variances, petal length and petal width
# def plotting(X: np.array, column_X: labels: np.array, centroids: np.array):
#      plt.scatter(X[:, 1], X[:, 2], c=labels)
#      plt.scatter(centroids[:, 1], centroids[:, 2], color='red')
#      plt.show()
     
     
