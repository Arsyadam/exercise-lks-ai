class PCA:
     def __init__(self, n_components=2):
          self.n_components = n_components
          self.mean = None 
          self._components = None 
          self._explained_variance = None 
          
     def fit(self, X):
          self.mean = X.mean()
          X = X - self.mean 
          
          # getting the cov matrix, but the data is being trasnpose first
          # because numpy wants the features in the index position
          cov = np.cov(X.T)
          
          # getting the eigenvalues and the eigenvector from the cov matrix
          eigenvalues, eigenvectors = np.linalg.eig(cov)
          
          # sorting the indices by descending order
          indices = np.argsort(eigenvalues)[::-1]
          eigenvalues = eigenvalues[indices]
          eigenvectors = eigenvectors[:, eigenvalues]
          
          self._components = eigenvectors[:, :self.n_components].T
          self._explained_variance = eigenvalues
          
     def transform(self, X):
          X = X - self.mean
          return np.dot(X, self._components.T)
     
     def _explained_variance_ration(self):
          total_variance = sum(self._explained_variance)
          return self._explained_variance / total_variance
     
