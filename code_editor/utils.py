import math
import random

def create_tfidf_matrix(documents):
    """
    Create a TF-IDF matrix from a list of documents.
    
    Args:
        documents: List of strings, each representing a document
        
    Returns:
        vocabulary: Dictionary mapping words to indices
        tfidf_matrix: List of TF-IDF vectors, one per document
    """
    # Create vocabulary
    vocabulary = {}
    word_index = 0
    for doc in documents:
        for word in doc.lower().split():
            if word not in vocabulary:
                vocabulary[word] = word_index
                word_index += 1
    
    # Calculate TF-IDF matrix
    tfidf_matrix = []
    for doc in documents:
        # Calculate term frequency
        tf = {}
        doc_words = doc.lower().split()
        doc_len = len(doc_words)
        for word in doc_words:
            tf[word] = tf.get(word, 0) + 1
        
        # Calculate TF-IDF vector
        tfidf_vector = [0] * len(vocabulary)
        for word, freq in tf.items():
            if word in vocabulary:
                # TF part
                tf_value = freq / max(doc_len, 1)  # Avoid division by zero
                
                # IDF part
                doc_with_term = sum(1 for d in documents if word in d.lower().split())
                idf_value = math.log((len(documents) + 1) / (doc_with_term + 1)) + 1
                
                # TF-IDF
                tfidf_vector[vocabulary[word]] = tf_value * idf_value
        
        # Normalize vector
        magnitude = math.sqrt(sum(x**2 for x in tfidf_vector))
        if magnitude > 0:
            tfidf_vector = [x/magnitude for x in tfidf_vector]
        
        tfidf_matrix.append(tfidf_vector)
    
    return vocabulary, tfidf_matrix


def kmeans_clustering(data, num_clusters, max_iterations=100, random_seed=42):
    """
    Perform K-means clustering on the given data.
    
    Args:
        data: List of vectors to cluster
        num_clusters: Number of clusters to form
        max_iterations: Maximum number of iterations to perform
        random_seed: Random seed for reproducibility
        
    Returns:
        clusters: List of cluster assignments for each data point
        centroids: List of cluster centroids
    """
    if not data or num_clusters <= 0 or num_clusters > len(data):
        return [], []
    
    # Initialize centroids randomly
    random.seed(random_seed)
    centroid_indices = random.sample(range(len(data)), num_clusters)
    centroids = [data[idx].copy() for idx in centroid_indices]
    
    # K-means clustering
    clusters = [0] * len(data)
    
    for _ in range(max_iterations):
        # Assign points to clusters
        prev_clusters = clusters.copy()
        for i, point in enumerate(data):
            min_dist = float('inf')
            cluster_idx = 0
            
            for j, centroid in enumerate(centroids):
                # Calculate Euclidean distance
                dist = math.sqrt(sum((p-c)**2 for p, c in zip(point, centroid)))
                if dist < min_dist:
                    min_dist = dist
                    cluster_idx = j
            
            clusters[i] = cluster_idx
        
        # Check for convergence
        if prev_clusters == clusters:
            break
        
        # Update centroids
        for j in range(num_clusters):
            cluster_points = [data[i] for i in range(len(data)) if clusters[i] == j]
            if cluster_points:
                # Calculate mean of points in cluster
                vector_length = len(data[0])
                centroid = [0] * vector_length
                for point in cluster_points:
                    for k in range(vector_length):
                        centroid[k] += point[k]
                
                centroids[j] = [x/len(cluster_points) for x in centroid]
    
    return clusters, centroids


def find_similar_profiles(user_profile, profiles, max_clusters=5):
    """
    Find profiles similar to the user profile based on interests using TF-IDF and K-means.
    
    Args:
        user_profile: User profile object with interests attribute
        profiles: List of other profile objects with interests attribute
        max_clusters: Maximum number of clusters to form
        
    Returns:
        similar_profiles: List of profiles similar to the user
    """
    if not profiles:
        return []
    
    # Extract interests
    all_interests = [user_profile.interests] + [profile.interests for profile in profiles]
    
    # Create TF-IDF matrix
    _, tfidf_matrix = create_tfidf_matrix(all_interests)
    
    # Determine number of clusters
    num_clusters = min(len(profiles), max_clusters)
    
    # Perform K-means clustering
    clusters, _ = kmeans_clustering(tfidf_matrix, num_clusters)
    
    # Get user's cluster
    user_cluster = clusters[0]
    
    # Find similar profiles (in the same cluster as the user)
    similar_profiles = [
        profiles[i] for i in range(len(profiles)) if clusters[i + 1] == user_cluster
    ]
    
    return similar_profiles