import numpy as np
import pandas as pd

data = input("Please provide path to dataset: ")

# Read the dataset and take a look at its contents
df = pd.read_csv(data)

# Extracting all locations
depot = (df["depot_lat"].values[0], df["depot_lng"].values[0])
customers = []
for customer in range(df.shape[0]):
  details = df.iloc[customer]
  customers.append([details.iloc[2], details.iloc[1], details.iloc[0]])
  
# Function for extracting distance
def haversine(lat1, lon1, lat2, lon2):
  R = 6371
  phi1 = np.radians(lat1)
  phi2 = np.radians(lat2)
  delta_phi = np.radians(lat2 - lat1)
  delta_lambda = np.radians(lon2 - lon1)
  a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
  res = R * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
  return np.round(res, 2)

# Creating a graph of distances
graph = []
for i in range(len(customers)+1):
  zeros = [0] * (len(customers)+1)
  graph.append(zeros)

for i in range(len(customers)+1):
  for j in range(i+1, len(customers)+1):
    if i == 0:
      dist = haversine(depot[0], depot[1], customers[j-1][0], customers[j-1][1])
    else:
      dist = haversine(customers[i-1][0], customers[i-1][1], customers[j-1][0], customers[j-1][1])
    graph[i][j] = dist
    graph[j][i] = dist


# Now that we have the graph, we can build an algorithm
def find_path(graph):
  path = [0]
  start = 0
  visit = [0]*len(graph)
  visit[start] = 1
  visited = 1
  while visited < len(graph):
    minimum = 1000
    end = -1
    for i in range(len(graph)):
      if visit[i] == 0 and graph[start][i] < minimum:
        minimum = graph[start][i]
        end = i
    start = end
    visited += 1
    visit[end] = 1
    path.append(end)
  return path
      
#print(find_path(graph, start, [0]*len(graph)))

# Making the output csv file
path = find_path(graph)[1:]
#print(path)
output = {"order_id":[], "lng":[], "lat":[], "depot_lat":[], "depot_lng":[], "dlvr_seq_num":[]}
for i in range(len(path)):
  output["order_id"].append(customers[path[i]-1][2])
  output["lng"].append(customers[path[i]-1][1])
  output["lat"].append(customers[path[i]-1][0])
  output["depot_lat"].append(depot[0])
  output["depot_lng"].append(depot[1])
  output["dlvr_seq_num"].append(i+1)

out = pd.DataFrame(output)
name = data.split("\\")
if len(name) == 1:
  name = data.split("/")
name[-1] = name[-1].replace("input", "output")
name[0] = "output_datasets"
name = "/".join(name)
out.to_csv(name, index=False)

# Test
min_path = find_path(graph)
path = min_path + [0]
print(path)
dist = 0
for i in range(len(path) - 1):
  dist += graph[path[i]][path[i+1]]
print(dist)
