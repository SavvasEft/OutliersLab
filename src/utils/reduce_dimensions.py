from sklearn.decomposition import PCA

def reduce_to_2d_PCA(data):
    # Apply PCA and reduce the dimensionality to 2 components
    pca = PCA(n_components=2)
    pca.fit(data)
    X_pca = pca.transform(data) 
    return X_pca