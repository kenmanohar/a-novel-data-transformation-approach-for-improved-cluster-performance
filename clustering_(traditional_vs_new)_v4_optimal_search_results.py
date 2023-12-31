# -*- coding: utf-8 -*-
"""Clustering (traditional vs new) v4 - Optimal Search Results.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qef0_lHthnkFVR1T1bg7HxCu4ntnijWB

*Version* 4

Used for thesis - generate scores for optimal kappas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from scipy.cluster.hierarchy import dendrogram, linkage

from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN

from sklearn import metrics
from sklearn.metrics import davies_bouldin_score

"""# Datasets

## Auto dataset
"""

# '''
# AUTO DATASET
# '''
# data = 'https://raw.githubusercontent.com/kenmanohar/stat6005/main/auto.csv'
# df = pd.read_csv(data)

# # Drop rows with null values
# df.dropna(inplace=True)
# df.reset_index(drop=True, inplace=True)

# # # Choose attributes
# subset_columns = ['cylinders', 'acc', 'mpg']
# df = df[subset_columns].copy()

# # Set target column
# target = 'mpg'

# # Extract attributes
# attributes = df.columns.tolist()
# attributes.remove(target)

# # Create copy for new clustering approach
# df2 = df.copy()

# # # Grid Search
# # kappas =	{'cylinders': 5, 'acc': 7, 'year': 48}

# # Successive Quadratic Approximation
# kappas =	{'cylinders': 11.5, 'acc': 5, 'year': 127.7}


# dist_metric = 'euclidean'

# num_clusters_trad = 3 # from elbow diagram
# num_clusters_new  = num_clusters_trad

# eps_trad = 2.3 # from knee point plot
# eps_new = eps_trad

"""## Insurance dataset"""

# '''
# INSURANCE DATASET
# '''
# # All columns = ['index', 'PatientID', 'age', 'gender', 'bmi', 'bloodpressure', 'diabetic', 'children', 'smoker', 'region', 'claims']

# data = 'https://raw.githubusercontent.com/kenmanohar/stat6005/main/insurance_data.csv'
# df = pd.read_csv(data)

# # Drop rows with null values
# df.dropna(inplace=True)
# df.reset_index(drop=True, inplace=True)

# # # Choose attributes
# # Remove 'index' and 'PatientID' columns
# subset_columns = ['age', 'gender', 'bmi', 'bloodpressure', 'diabetic', 'children', 'smoker', 'region', 'claims']
# df = df[subset_columns].copy()

# # Set target column
# target = 'claims'

# # Extract attributes
# attributes = df.columns.tolist()
# attributes.remove(target)

# # Create copy for new clustering approach
# df2 = df.copy()

# # Grid Search
# #kappas =	{'age':3, 'gender':0, 'bmi':2, 'bloodpressure':5, 'diabetic':0, 'children':0, 'smoker':1, 'region':1}

# # Successive Quadratic Approximation
# kappas =	{'age':1, 'gender':0, 'bmi':0.5, 'bloodpressure':4.5, 'diabetic':0, 'children':0, 'smoker':0.3, 'region':0.4}

# dist_metric = 'euclidean'

# num_clusters_trad = 2 # from elbow plot
# num_clusters_new  = num_clusters_trad

# eps_trad = 3.1 # From knee point plot
# eps_new = eps_trad

"""## Student Math dataset"""

'''
STUDENT MATH DATASET
'''

data = 'https://raw.githubusercontent.com/kenmanohar/stat6005/main/student_math.csv'
df = pd.read_csv(data)

# Drop rows with null values
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

subset_columns = ['G2', 'G1', 'failures', 'absences', 'age', 'G3']
df = df[subset_columns].copy()

# Set target column
target = 'G3'

# Extract attributes
attributes = df.columns.tolist()
attributes.remove(target)

# Create copy for new clustering approach
df2 = df.copy()

# # Grid Search
# kappas =	{'G2':6, 'G1':6, 'failures':6, 'absences':12, 'age':6,
#           'school':6,	'sex':6,	'address':6,	'famsize':6,	'Pstatus':6,	'Medu':6,	'Fedu':6,	'Mjob':6,	'Fjob':6,
#           'reason':6,	'guardian':6,	'traveltime':6,	'studytime':6,	'schoolsup':6,	'famsup':6,	'paid':6,	'activities':6,
#           'nursery':6,	'higher':6,	'internet':6,	'romantic':6,	'famrel':6,	'freetime':6,	'goout':6,	'Dalc':6,	'Walc':6,	'health':6}

# Successive Quadratic Approximation
kappas =	{'G1':10.5, 'G2':65.6, 'failures':48.8, 'absences':178.5, 'age':100}

dist_metric = 'euclidean'

num_clusters_trad = 4 # from elbow diagram
num_clusters_new  = num_clusters_trad

eps_trad = 9 # from knee point plot
eps_new = eps_trad

df

df2

"""# Traditional Clustering Approach

## Normalization
"""

for a in df.columns.tolist():

  # Use StandardScaler for numerical attributes
  if df[a].dtype == 'int64' or df[a].dtype == 'float64':

    scaler = StandardScaler()
    df[a] = scaler.fit_transform(df[[a]])

  # Use one-hot encoding for categorical attributes
  elif df[a].dtype == 'object':

    df = pd.get_dummies(df, columns=[a])

  else:
    print("Unknown column type")

df

"""## Elbow diagram"""

# from enum import auto
# # Calculate and plot inertia for different numbers of clusters
# inertia_values = []
# max_clusters = 10

# for num_clusters in range(1, max_clusters + 1):
#     kmeans = KMeans(n_clusters=num_clusters, random_state=0, n_init='auto')
#     kmeans.fit(df)
#     inertia_values.append(kmeans.inertia_)

# # Plot the elbow curve
# plt.figure(figsize=(8, 6))
# plt.plot(range(1, max_clusters + 1), inertia_values, marker='o')
# plt.xlabel('Number of Clusters')
# plt.ylabel('Inertia')
# plt.title('Elbow Method for Traditional Clustering of '+target)
# plt.xticks(range(1, max_clusters + 1))
# plt.show()

"""## Dendrogram"""

# linkage_matrix = linkage(df, method ='ward') # method ='single', 'complete', 'ward', 'average')

# # Plot the dendrogram
# plt.figure(figsize=(10, 6))
# dendrogram(linkage_matrix, labels=np.array(df.index), orientation='top')
# plt.xlabel("Sample Index")
# plt.ylabel("Distance")
# plt.title("Dendrogram for Traditional Clustering of "+target)
# plt.show()

"""## Knee Point"""

# # Create a NearestNeighbors object to compute nearest neighbor distances
# neighbors = NearestNeighbors(n_neighbors=10)
# neighbors.fit(df)
# distances, _ = neighbors.kneighbors(df)

# # Sort the distances and plot the k-distance graph
# sorted_distances = np.sort(distances[:, -1])
# plt.plot(sorted_distances)

# # Find the knee/elbow point (optimal epsilon)
# knee_point_index = np.argmax(np.diff(sorted_distances)) + 1
# knee_point_distance = sorted_distances[knee_point_index]

# # Plot the knee point on the graph
# plt.plot(knee_point_index, knee_point_distance, 'ro', label='Knee Point')
# plt.xlabel('Number of Neighbors')
# plt.ylabel('Distance')
# plt.title('K-Distance for Traditional Clustering of '+ target)
# plt.legend()
# plt.show()

# print("Optimal eps (knee point distance):", knee_point_distance)

"""## KMeans"""

# Initialize KMeans clustering model

kmeans_trad = df.copy()
kmeans_clustering = KMeans(n_clusters=num_clusters_trad, random_state = 0, n_init='auto', )

# Fit-predict method
kmeans_trad["cluster"] = kmeans_clustering.fit_predict(kmeans_trad)

"""## Agglomerative"""

# Initialize Agglomerative clustering model

agg_trad = df.copy()
agg_clustering = AgglomerativeClustering(n_clusters=num_clusters_trad, metric=dist_metric)

# Fit-predict method
agg_trad["cluster"] = agg_clustering.fit_predict(agg_trad)

"""## DBSCAN"""

# Initialize DBSCAN clustering model

dbscan_trad = df.copy()
dbscan_clustering = DBSCAN(eps=eps_trad, metric=dist_metric)

# Fit-predict method
dbscan_trad["cluster"] = dbscan_clustering.fit_predict(dbscan_trad)

"""# New Clustering Approach

## Weighted Averages
"""

# Function to find weighted averages

def weighted_averages(_kappa, _df, _feature_avg_val, _target, _averages):

  weighted_target_by_attribute ={}

  for _f in _averages:

    _sample_feature_avg_val = _averages[_f]
    _df['_weights'] = 1/(1+(_df[_feature_avg_val] - _sample_feature_avg_val).abs() )**_kappa
    _df['_weighted_target'] = _df['_weights']* _df[_target]
    _sample_feature_weighted_avg = _df['_weighted_target'].sum()/_df['_weights'].sum()
    weighted_target_by_attribute[_f] = _sample_feature_weighted_avg

  _df.drop('_weights', axis=1, inplace=True)
  _df.drop('_weighted_target', axis=1, inplace=True)

  return weighted_target_by_attribute

for a in attributes:

  # Numerical attribute
  if df2[a].dtype == 'int64' or df2[a].dtype == 'float64':
    #print(f"{a} is Numerical with kappa {kappas[a]}")

    for i in range(0, len(df2)):
      sum_of_differences = 0

      for j in range(0, len(df2)):
        sum_of_differences += (df2.at[i, a] - df2.at[j, a])**2

      df2.at[i, "distances"] = sum_of_differences*0.5

      df2["weights"] = 1/(1 + df2["distances"])**kappas[a]

      df2["weighted target"] = df2["weights"] * df2[a]

      df2.at[i, "weighted_"+a] = df2["weighted target"].sum() / df2["weights"].sum()

    # Remove original attribute column
    df2.drop(a, axis=1, inplace=True)

    df2.drop("distances", axis=1, inplace=True)
    df2.drop("weights", axis=1, inplace=True)
    df2.drop("weighted target", axis=1, inplace=True)


  # Categorical attribute
  #
  elif df2[a].dtype == 'object':
    #print(f"{a} is Categorical with kappa {kappas[a]}")

    # Find means for all values of each attribute
    averages = df2.groupby(a)[target].mean().to_dict()

    # New column with all values of each attribute with their corresponding mean
    df2['avg_'+a] = df2[a].map(averages)

    weighted_avgs = weighted_averages(kappas[a], df2, 'avg_'+a, target, averages)

    # New column with all means of each attributed with their corresponding weighted average
    df2['weighted_avg_'+a] = df2[a].map(weighted_avgs)

    # Remove original attribute column
    df2.drop(a, axis=1, inplace=True)

    # Remove column with all values of each attribute with their corresponding mean
    df2.drop('avg_'+a, axis=1, inplace=True)

  else:
    print("Unknown column type")

df2

# feature_x = 'weighted_cylinders'
# feature_y = 'mpg'

# plt.figure(figsize=(10, 6))

# # Plot a line chart
# plt.plot(df2[feature_x], df2[feature_y], marker='o', linestyle='-', color='b', label='Line Chart')

# # Add labels and title
# plt.xlabel(feature_x)
# plt.ylabel(feature_y)
# plt.title('Line Chart of ' + feature_x + ' vs ' + feature_y)

# # Add legend
# plt.legend()

# # Show the plot
# plt.show()

# feature_x = 'weighted_acc'
# feature_y = 'mpg'

# plt.figure(figsize=(10, 6))

# # Plot a line chart
# plt.plot(df2[feature_x], df2[feature_y], marker='o', linestyle='-', color='b', label='Line Chart')

# # Add labels and title
# plt.xlabel(feature_x)
# plt.ylabel(feature_y)
# plt.title('Line Chart of ' + feature_x + ' vs ' + feature_y)

# # Add legend
# plt.legend()

# # Show the plot
# plt.show()

# feature_x = 'weighted_year'
# feature_y = 'mpg'

# plt.figure(figsize=(10, 6))

# # Plot a line chart
# plt.plot(df2[feature_x], df2[feature_y], marker='o', linestyle='-', color='b', label='Line Chart')

# # Add labels and title
# plt.xlabel(feature_x)
# plt.ylabel(feature_y)
# plt.title('Line Chart of ' + feature_x + ' vs ' + feature_y)

# # Add legend
# plt.legend()

# # Show the plot
# plt.show()



"""## Elbow diagram"""

# from enum import auto
# # Calculate and plot inertia for different numbers of clusters
# inertia_values = []
# max_clusters = 10

# for num_clusters in range(1, max_clusters + 1):
#     kmeans = KMeans(n_clusters=num_clusters, random_state=0, n_init='auto')
#     kmeans.fit(df2)
#     inertia_values.append(kmeans.inertia_)

# # Plot the elbow curve
# plt.figure(figsize=(8, 6))
# plt.plot(range(1, max_clusters + 1), inertia_values, marker='o')
# plt.xlabel('Number of Clusters')
# plt.ylabel('Inertia')
# plt.title('Elbow Method for New Clustering of '+target)
# plt.xticks(range(1, max_clusters + 1))
# plt.show()

"""## Dendrogram"""

# linkage_matrix = linkage(df2, method ='ward') # method ='single', 'complete', 'ward', 'average')

# # Plot the dendrogram
# plt.figure(figsize=(10, 6))
# dendrogram(linkage_matrix, labels=np.array(df2.index), orientation='top')
# plt.xlabel("Sample Index")
# plt.ylabel("Distance")
# plt.title("Dendrogram for New Clustering of "+target)
# plt.show()

"""## Knee Point"""

# # Create a NearestNeighbors object to compute nearest neighbor distances
# neighbors = NearestNeighbors(n_neighbors=10)
# neighbors.fit(df2)
# distances, _ = neighbors.kneighbors(df2)

# # Sort the distances and plot the k-distance graph
# sorted_distances = np.sort(distances[:, -1])
# plt.plot(sorted_distances)

# # Find the knee/elbow point (optimal epsilon)
# knee_point_index = np.argmax(np.diff(sorted_distances)) + 1
# knee_point_distance = sorted_distances[knee_point_index]

# # Plot the knee point on the graph
# plt.plot(knee_point_index, knee_point_distance, 'ro', label='Knee Point')
# plt.xlabel('Number of Neighbors')
# plt.ylabel('Distance')
# plt.title('K-Distance for Traditional Clustering of '+ target)
# plt.legend()
# plt.show()

# print("Optimal eps (knee point distance):", knee_point_distance)

"""## KMeans"""

# Initialize KMeans clustering model

kmeans_new = df2.copy()
kmeans_clustering2 = KMeans(n_clusters=num_clusters_new, random_state = 0, n_init='auto')

# Fit-predict method
kmeans_new["cluster"] = kmeans_clustering2.fit_predict(kmeans_new)

"""## Agglomerative"""

# Initialize Agglomerative clustering model

agg_new = df2.copy()
agg_clustering2 = AgglomerativeClustering(n_clusters=num_clusters_new, metric=dist_metric)

# Fit-predict method
agg_new["cluster"] = agg_clustering2.fit_predict(agg_new)

"""## DBSCAN"""

# Initialize DBSCAN clustering model

dbscan_new = df2.copy()
dbscan_clustering2 = DBSCAN(eps=eps_new, metric=dist_metric)

# Fit-predict method
dbscan_new["cluster"] = dbscan_clustering2.fit_predict(dbscan_new)

"""# Results

## Cluster Sizes
"""

# KMeans clusters

print("KMeans (Traditional)")
print(kmeans_trad['cluster'].value_counts())
print()
print("KMeans (New)")
print(kmeans_new['cluster'].value_counts())
print("\n")


# Agglomerative clusters

print("Agglomerative (Traditional)")
print(agg_trad['cluster'].value_counts())
print()
print("Agglomerative (New)")
print(agg_new['cluster'].value_counts())
print("\n")


# DBSCAN clusters

print("DBSCAN (Traditional)")
print(dbscan_trad['cluster'].value_counts())
print()
print("DBSCAN (New)")
print(dbscan_new['cluster'].value_counts())

"""## Scores"""

scores = pd.DataFrame(columns=["Algorithm", "Approach", "Silhouette Coefficient", "Calinski-Harabasz Index", "Davies-Bouldin Index"])

# KMeans scores (Traditional)
scores.loc[len(scores.index)] = ["KMeans",
                                 "Traditional",
                                 metrics.silhouette_score(kmeans_trad, kmeans_trad["cluster"]),
                                 metrics.calinski_harabasz_score(kmeans_trad, kmeans_trad["cluster"]),
                                 davies_bouldin_score(kmeans_trad, kmeans_trad["cluster"])]

# KMeans scores (New)
scores.loc[len(scores.index)] = ["KMeans",
                                 "New",
                                 metrics.silhouette_score(kmeans_new, kmeans_new["cluster"]),
                                 metrics.calinski_harabasz_score(kmeans_new, kmeans_new["cluster"]),
                                 davies_bouldin_score(kmeans_new, kmeans_new["cluster"])]



# Agglomerative scores (Traditional)
scores.loc[len(scores.index)] = ["Agglomerative",
                                 "Traditional",
                                 metrics.silhouette_score(agg_trad, agg_trad["cluster"]),
                                 metrics.calinski_harabasz_score(agg_trad, agg_trad["cluster"]),
                                 davies_bouldin_score(agg_trad, agg_trad["cluster"])]

# Agglomerative scores (New)
scores.loc[len(scores.index)] = ["Agglomerative",
                                 "New",
                                 metrics.silhouette_score(agg_new, agg_new["cluster"]),
                                 metrics.calinski_harabasz_score(agg_new, agg_new["cluster"]),
                                 davies_bouldin_score(agg_new, agg_new["cluster"])]


# DBSCAN scores (Traditional)
if len(dbscan_trad["cluster"].unique()) == 1:
  scores.loc[len(scores.index)] = ["DBSCAN",
                                   "Traditional",
                                   "N/A",
                                   "N/A",
                                   "N/A"]
else:
  scores.loc[len(scores.index)] = ["DBSCAN",
                                  "Traditional",
                                  metrics.silhouette_score(dbscan_trad, dbscan_trad["cluster"]),
                                  metrics.calinski_harabasz_score(dbscan_trad, dbscan_trad["cluster"]),
                                  davies_bouldin_score(dbscan_trad, dbscan_trad["cluster"])]

# DBSCAN scores (New)
if len(dbscan_new["cluster"].unique()) == 1:
  scores.loc[len(scores.index)] = ["DBSCAN",
                                   "New",
                                   "N/A",
                                   "N/A",
                                   "N/A"]
else:
  scores.loc[len(scores.index)] = ["DBSCAN",
                                  "New",
                                  metrics.silhouette_score(dbscan_new, dbscan_new["cluster"]),
                                  metrics.calinski_harabasz_score(dbscan_new, dbscan_new["cluster"]),
                                  davies_bouldin_score(dbscan_new, dbscan_new["cluster"])]

# Show results
scores.round(3)

scores_trad = pd.DataFrame(columns=["Algorithm", "Approach", "Silhouette Coefficient", "Calinski-Harabasz Index", "Davies-Bouldin Index", "Cluster Sizes"])

# KMeans scores (Traditional)
scores_trad.loc[len(scores_trad.index)] = ["KMeans",
                                            "Traditional",
                                            metrics.silhouette_score(kmeans_trad, kmeans_trad["cluster"]),
                                            metrics.calinski_harabasz_score(kmeans_trad, kmeans_trad["cluster"]),
                                            davies_bouldin_score(kmeans_trad, kmeans_trad["cluster"]),
                                            kmeans_trad['cluster'].value_counts()
                                          ]

# Agglomerative scores (Traditional)
scores_trad.loc[len(scores_trad.index)] = ["Agglomerative",
                                            "Traditional",
                                            metrics.silhouette_score(agg_trad, agg_trad["cluster"]),
                                            metrics.calinski_harabasz_score(agg_trad, agg_trad["cluster"]),
                                            davies_bouldin_score(agg_trad, agg_trad["cluster"]),
                                            agg_trad['cluster'].value_counts()
                                          ]


# DBSCAN scores (Traditional)
if len(dbscan_trad["cluster"].unique()) == 1:
  scores_trad.loc[len(scores_trad.index)] = ["DBSCAN",
                                              "Traditional",
                                              "N/A",
                                              "N/A",
                                              "N/A",
                                              "N/A"
                                        ]
else:
  scores_trad.loc[len(scores_trad.index)] = ["DBSCAN",
                                              "Traditional",
                                              metrics.silhouette_score(dbscan_trad, dbscan_trad["cluster"]),
                                              metrics.calinski_harabasz_score(dbscan_trad, dbscan_trad["cluster"]),
                                              davies_bouldin_score(dbscan_trad, dbscan_trad["cluster"]),
                                              dbscan_trad['cluster'].value_counts()
                                              ]

scores_new = pd.DataFrame(columns=["Algorithm", "Approach", "Silhouette Coefficient", "Calinski-Harabasz Index", "Davies-Bouldin Index", "Cluster Sizes"])

# KMeans scores (New)
scores_new.loc[len(scores_new.index)] = ["KMeans",
                                          "New",
                                          metrics.silhouette_score(kmeans_new, kmeans_new["cluster"]),
                                          metrics.calinski_harabasz_score(kmeans_new, kmeans_new["cluster"]),
                                          davies_bouldin_score(kmeans_new, kmeans_new["cluster"]),
                                          kmeans_new['cluster'].value_counts()
                                          ]

# Agglomerative scores (New)
scores_new.loc[len(scores_new.index)] = ["Agglomerative",
                                          "New",
                                          metrics.silhouette_score(agg_new, agg_new["cluster"]),
                                          metrics.calinski_harabasz_score(agg_new, agg_new["cluster"]),
                                          davies_bouldin_score(agg_new, agg_new["cluster"]),
                                          agg_new['cluster'].value_counts()
                                          ]

# DBSCAN scores (New)
if len(dbscan_new["cluster"].unique()) == 1:
  scores_new.loc[len(scores_new.index)] = ["DBSCAN",
                                            "New",
                                            "N/A",
                                            "N/A",
                                            "N/A",
                                            "N/A"
                                            ]
else:
  scores_new.loc[len(scores_new.index)] = ["DBSCAN",
                                            "New",
                                            metrics.silhouette_score(dbscan_new, dbscan_new["cluster"]),
                                            metrics.calinski_harabasz_score(dbscan_new, dbscan_new["cluster"]),
                                            davies_bouldin_score(dbscan_new, dbscan_new["cluster"]),
                                            dbscan_new['cluster'].value_counts()
                                            ]

scores_trad.round(3)

scores_new.round(3)

attributes