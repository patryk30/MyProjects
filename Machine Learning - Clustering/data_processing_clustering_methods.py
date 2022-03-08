# -*- coding: utf-8 -*-
"""
Przetwarzanie i analiza danych w programie Python - Projekt 2/3
Plik generujacy pliki .csv oraz .png z wykresami
"""

########## pakiety ##########
import sys, os.path
import numpy as np
import glob
import re
from collections import namedtuple
import numpy as np
import pandas as pd

import genieclust
import matplotlib.pyplot as plt
plt.rcParams["image.cmap"] = "viridis"

from sklearn.cluster import KMeans #metoda k-srednich
from sklearn.metrics import fowlkes_mallows_score #indeks Fowlkesa–Mallowsa (FM)
from sklearn.metrics import adjusted_rand_score #skorygowany indeks Randa (AR)
from sklearn.cluster import AgglomerativeClustering #metody hierarchiczne
from sklearn.cluster import DBSCAN #Density-Based Spatial Clustering of Applications with Noise
from sklearn.preprocessing import StandardScaler

import csv



##############################################
def load_dataset(name, path="."):
    """Loads a dataset named `name` relative to the directory `path`.
    Arguments
    =========
    name
        dataset name
    path
        path to the downloaded suite, defaults to the current working dir
    Returns
    =======
    A named tuple with the following elements:
        data
            data matrix
        labels
            a list with at least one label vectors
        name
            same as the `name` argument
    Examples
    ========
    import os.path
    data, labels, name = load_dataset(os.path.join("wut", "smile"),
        "/usr/share/clustering_benchmarks_v1")
    ret = load_dataset("smile", "/usr/share/clustering_benchmarks_v1/wut")
    print(ret.data, ret.labels, ret.name)
    """
    base_name = os.path.join(path, name)

    data_file = base_name+".data.gz"
    data = np.loadtxt(data_file, ndmin=2)
    labels_files = sorted(glob.glob(base_name+".labels?.gz"))
    assert len(labels_files) > 0

    labels = [
        np.loadtxt(labels_file, dtype='int')
        for labels_file in labels_files
    ]

    RetClass = namedtuple("ClusteringBenchmark", ["data", "labels", "name"])
    return RetClass(data=data, labels=labels, name=name)




def Mnn(X, M):
    """
    funkcja wyznacza macierz M najblizszych sasiadow kazdego punktu
    """
    n = X.shape[0]
    
    S = np.zeros(shape=[n,M]) #definiujemy pusta tablice (macierz zer)
    S_help = np.zeros(shape=[n,n])
    
    for i in range(n):
        j=n-1
        while j>=i:
            S_help[i][j] = np.sum(np.square(X[i,:]-X[j,:]))
            S_help[j][i] = S_help[i][j]
            j -= 1
        
        S_help[i][i] = np.max(S_help[i,:])+1
        for j in range(M):
            a = np.where(S_help[i,:]==np.min(S_help[i,:]))[0][0]
            S[i][j] = a
            S_help[i][a] = np.max(S_help[i,:])+1
            
    return S


##algorytm przeszukiwania w glab DFS
def DFS(G,v,visited,result):
    """
    Implementacja algorytmu przeszukiwania w glab
    Funkcja przyjmuje jako argumenty:
        - symetryczna macierz sasiedztwa grafu
        - wierzcholek poczatkowy
        - lista 'visited' informujaca ktore wierzcholki juz zostaly odwiedzone
        - argument 'result' jest aktualizowana lista wierzcholkow w spojnym podgrafie
        (algorymt na bazie rekurencji)
    Zwraca spojna skladowa grafu
    
    Uwaga: numery wierzcholkow zaczynamy od zera 
    """
    visited[v] = True
    
    result.append(v)
    
    for i in range(len(G[v])):
        if G[v][i] == 1: #w grafie z zadania to oznacza sasiedztwo wierzcholkow
            if visited[i] == False:
                result = DFS(G,i,visited,result)
    
    return result


##funkcja znajdujaca wszystkie spojne skladowe grafu
def connected_components(G):
    """
    Korzystajac z funkcji DFS, funkcja ta zwraca wszystkie spojne skladowe grafu G
    argument: macierz sasiedztwa G
    Funkcja zwraca liste skladajaca sie z list wierzcholkow bedacych w tej samej skladowej
    """
    visited = [False]*len(G)
    components = []
    
    for i in range(len(G)):
        if visited[i] == False:
            result = []
            components.append(DFS(G,i,visited,result))
    return components

def Mnn_graph(S):
    n= S.shape[0]
    G = np.zeros(shape=[n,n])
    
    for i in range(n):
        for j in range(S.shape[1]):
            b = int(S[i][j])
            if i in S[b]:
                G[i][b] = 1
                G[b][i] = 1
                
    #wykrywamy spojne skladowe
    components = connected_components(G)
    if len(components) == 1:
        return G
    else:
        a = components[0][0]
        for i in range(1, len(components)):
            G[a][components[i][0]] = 1
            G[components[i][0]][a] = 1
        return G

def Laplacian_eigen(G, k):
    """
    Funkcja zwraca macierz E skladajaca sie z wektorow wlasnych laplasjanu grafu G 
    odpowiadajacych 2,3,4,...,(k+1) najmniejszej wartosci wlasnej
    
    argumenty:
        -macierz sasiedztwa grafu G (wymiar nxn)
        -integer k 
    """
    
    n = G.shape[0]
    
    if k<=1 or k>n:
        raise Exception("Incorrect value of k")
        
    D = np.zeros(shape=[n,n])
    
    for i in range(n):
        D[i][i] = np.sum(G[i,:])
    
    L = D-G
    
    E_eigval = np.linalg.eig(L)[0]
    E_eigvect = np.linalg.eig(L)[1] #wektory wlasne to kolumny tablicy
        
    if k==n:
        E = E_eigvect
    else:
        index = []
        
        for i in range(k):
            #najpierw wykluczmy pierwsza najmniejsza wartosc wlasna
            E_eigval[np.where(E_eigval==np.min(E_eigval))] = np.max(E_eigval)+1
            
            #zapisujemy indeksy kolejnych najmniejszych wartosci wlasnych
            index.append(np.where(E_eigval==np.min(E_eigval))[0][0])
        
        E = E_eigvect[:, index] 
    
    return np.real(E)
   
    
#funckja docelowa dla algorytmu spektralego
def spectral_clustering(X, k, M):
    """
    funkcja sklada sie z procedur wywolywania poprzednio napisanych fukcji
    'Mnn(X, M)', 'Mnn_graph(S)', 'Laplacian_eigen(G, k)' oraz wywolaniu na wynikowym
    zbiorze algorytmu k-srednich z pakietu sklearn
    """
    
    S = Mnn(X, M)
    G = Mnn_graph(S)
    E = Laplacian_eigen(G, k)
    
    kmeans = KMeans(n_clusters=k).fit_predict(E)
    
    return kmeans


#porownanie dzialania roznych metod klasteryzacji na danym zbiorze
def compare_methods(k, X, y, spectral=True):
    """
    Parameters
    ----------
    k : TYPE: integer > 1, liczba klastrów
    X : TYPE: numpy array, dane benchmarkowe do grupowania
    y : TYPE: numpy array, etykiety do porownywania
    spectral : TYPE: bool, True - stosujemy algorytm spektralny, false - nie stosujemy

    Returns
    -------
    index_ARI : lista wspolczynnikow ARI dla kazdej metody
    index_FMI : lista wspolczynnikow FMI dla kazdej metody
    predictions : lista etykiet zwroconych przez kazda metode

    """
    
    if k<=1:
        raise Exception("Nieprawidłowa wartosc k")
        
    index_FMI = []
    index_ARI = []
    predictions = []
    
    kmeans_pred = KMeans(n_clusters=k).fit_predict(X)
    kmeans_ARI = adjusted_rand_score(y, kmeans_pred)
    kmeans_FMI = fowlkes_mallows_score(labels_true=y, labels_pred=kmeans_pred)
    index_FMI.append(kmeans_FMI)
    index_ARI.append(kmeans_ARI)
    predictions.append(kmeans_pred)
    
    hier_var_pred = AgglomerativeClustering(n_clusters=k, linkage='ward').fit_predict(X)
    #‘ward’ minimizes the variance of the clusters being merged
    hier_var_ARI = adjusted_rand_score(y, hier_var_pred)
    kmeans_var_FMI = fowlkes_mallows_score(y, hier_var_pred)
    index_FMI.append(kmeans_var_FMI)
    index_ARI.append(hier_var_ARI)
    predictions.append(hier_var_pred)
    
    hier_avg_pred = AgglomerativeClustering(n_clusters=k, linkage='average').fit_predict(X)
    #‘average’ uses the average of the distances of each observation of the two sets
    hier_avg_ARI = adjusted_rand_score(y, hier_avg_pred)
    kmeans_avg_FMI = fowlkes_mallows_score(y, hier_avg_pred) 
    index_FMI.append(kmeans_avg_FMI)
    index_ARI.append(hier_avg_ARI)
    predictions.append(hier_avg_pred)
    
    hier_single_pred = AgglomerativeClustering(n_clusters=k, linkage='single').fit_predict(X)
    #‘single’ uses the minimum of the distances between all observations of the two sets
    hier_single_ARI = adjusted_rand_score(y, hier_single_pred)
    kmeans_single_FMI = fowlkes_mallows_score(y, hier_single_pred)
    index_FMI.append(kmeans_single_FMI)
    index_ARI.append(hier_single_ARI)
    predictions.append(hier_single_pred)
    
    hier_comp_pred = AgglomerativeClustering(n_clusters=k, linkage='complete').fit_predict(X)
    #‘complete’ or ‘maximum’ linkage uses the maximum distances 
    #   between all observations of the two sets
    hier_comp_ARI = adjusted_rand_score(y, hier_comp_pred)
    kmeans_comp_FMI = fowlkes_mallows_score(y, hier_comp_pred)
    index_FMI.append(kmeans_comp_FMI)
    index_ARI.append(hier_comp_ARI)
    predictions.append(hier_comp_pred)
    
    genie_pred = genieclust.Genie(n_clusters=k).fit_predict(X)
    genie_ARI = adjusted_rand_score(y, genie_pred)
    genie_FMI = fowlkes_mallows_score(y, genie_pred)
    index_FMI.append(genie_FMI)
    index_ARI.append(genie_ARI)
    predictions.append(genie_pred)

    dbscan_pred = DBSCAN().fit_predict(X)
    dbscan_ARI = adjusted_rand_score(y, dbscan_pred)
    dbscan_FMI = fowlkes_mallows_score(y, dbscan_pred)
    index_FMI.append(dbscan_FMI)
    index_ARI.append(dbscan_ARI)
    predictions.append(dbscan_pred)
    
    if spectral == True:
        M = [int(X.shape[0]*0.01),int(X.shape[0]*0.05),int(X.shape[0]*0.1),int(X.shape[0]*0.3)]
        for i in M:
            spectral_pred = spectral_clustering(X,k,i)
            spectral_ARI = adjusted_rand_score(y, spectral_pred)
            spectral_FMI = fowlkes_mallows_score(y, spectral_pred)
            index_FMI.append(spectral_FMI)
            index_ARI.append(spectral_ARI)
            predictions.append(spectral_pred)

    return index_ARI, index_FMI, predictions


############# wykresy ###################

def wykres_2d(data, labels, file_name, path):
    plt.figure()
    plt.figure(figsize=(8,8))
    plt.scatter(data[:,0], data[:,1], c=labels)
    _fig_name = file_name +'_'+  str(len(np.unique(labels))) + "_main" + ".png"
    _fig_path = os.path.join(path, _fig_name)
    plt.savefig(_fig_path, format='png', transparent=True,
                    bbox_inches='tight', dpi=150)
    plt.close()
    
    return


def wykres_3d(data, labels, file_name, path):
    
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Generate the values
    x_vals = data[:, 0]
    y_vals = data[:, 1]
    z_vals = data[:, 2]
    
    # Plot the values
    ax.scatter(x_vals, y_vals, z_vals, c = labels , marker='o')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    
    _fig_name = file_name +'_'+ str(len(np.unique(labels))) + "_main" + ".png"
    _fig_path = os.path.join(path, _fig_name)
    fig.savefig(_fig_path, format='png', transparent=True,
                    bbox_inches='tight', dpi=150)
    plt.close()
    
    return


def wykres2(x,y,pred, titles, true_pred, file_name, path):
    """
    porównanie wyników algorytmów klasteryzacji na danym zbiorze w dwóch wymiarach
    """
    fig, axs = plt.subplots(4, 2, figsize=(10,15))
    fig.tight_layout()
    
    axs[0, 0].scatter(x, y, c=pred[0])
    axs[0, 0].set_title(titles[0])
    
    axs[0, 1].scatter(x, y, c=pred[1])
    axs[0, 1].set_title(titles[1])
    
    axs[1, 0].scatter(x, y, c=pred[2])
    axs[1, 0].set_title(titles[2])
    
    axs[1, 1].scatter(x, y, c=pred[3])
    axs[1, 1].set_title(titles[3])
    
    axs[2, 0].scatter(x, y, c=pred[4])
    axs[2, 0].set_title(titles[4])
    
    axs[2, 1].scatter(x, y, c=pred[5])
    axs[2, 1].set_title(titles[5])
    
    axs[3, 0].scatter(x, y, c=pred[6])
    axs[3, 0].set_title(titles[6])
    
    axs[3, 1].scatter(x, y, c=true_pred)
    axs[3, 1].set_title("True labels")

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
        
    _fig_name = file_name +'_'+  str(len(np.unique(true_pred))) + "_builtin_methods" + ".png"
    _fig_path = os.path.join(path, _fig_name)
    fig.savefig(_fig_path, format='png', transparent=True,
                    bbox_inches='tight', dpi=150)
    plt.close()
    
    return


def wykres3(x,y,z, labels, titles, true_label, file_name, path):
    """
    porównanie wyników zaimportowanych algorytmów klasteryzacji 
    na danym zbiorze w trzech wymiarach
    """
    fig = plt.figure(figsize=(15,13))

    ax = fig.add_subplot(331, projection='3d')
    ax.scatter(x, y, z, c = labels[0] , marker='o')
    ax.set_title(titles[0])
    
    ax = fig.add_subplot(332, projection='3d')
    ax.scatter(x, y, z, c = labels[1] , marker='o')
    ax.set_title(titles[1])
    
    ax = fig.add_subplot(333, projection='3d')
    ax.scatter(x, y, z, c = labels[2] , marker='o')
    ax.set_title(titles[2])
    
    ax = fig.add_subplot(334, projection='3d')
    ax.scatter(x, y, z, c = labels[3] , marker='o')
    ax.set_title(titles[3])
    
    ax = fig.add_subplot(335, projection='3d')
    ax.scatter(x, y, z, c = labels[4] , marker='o')
    ax.set_title(titles[4])
    
    ax = fig.add_subplot(336, projection='3d')
    ax.scatter(x, y, z, c = labels[5] , marker='o')
    ax.set_title(titles[5])
    
    ax = fig.add_subplot(337, projection='3d')
    ax.scatter(x, y, z, c = labels[6] , marker='o')
    ax.set_title(titles[6])
    
    ax = fig.add_subplot(338, projection='3d')
    ax.scatter(x, y, z, c = true_label , marker='o')
    ax.set_title("True labels")
    
    _fig_name = file_name +'_'+  str(len(np.unique(labels))) + "_bulitin_methods" + ".png"
    _fig_path = os.path.join(path, _fig_name)
    fig.savefig(_fig_path, format='png', transparent=True,
                    bbox_inches='tight', dpi=150)
    
    return


def wykres4(x,y,z, labels, titles, true_label, file_name, path):
    """
    porównanie wyników algorytmów spektralnych klasteryzacji 
    na danym zbiorze w dwóch wymiarach
    """
    fig = plt.figure(figsize=(15,13))

    ax = fig.add_subplot(221, projection='3d')
    ax.scatter(x, y, z, c = labels[-4] , marker='o')
    ax.set_title(titles[-4])
    
    ax = fig.add_subplot(222, projection='3d')
    ax.scatter(x, y, z, c = labels[-3] , marker='o')
    ax.set_title(titles[-3])
    
    ax = fig.add_subplot(223, projection='3d')
    ax.scatter(x, y, z, c = labels[-2] , marker='o')
    ax.set_title(titles[-2])
    
    ax = fig.add_subplot(224, projection='3d')
    ax.scatter(x, y, z, c = labels[-1] , marker='o')
    ax.set_title(titles[-1])
    
    _fig_name = file_name +'_'+ str(len(np.unique(labels))) + "_spectral_algorithm" + ".png"
    _fig_path = os.path.join(path, _fig_name)
    fig.savefig(_fig_path, format='png', transparent=True,
                    bbox_inches='tight', dpi=150) 
    
    return


def wykres5(data, labels, file_name, path):
    """
    Wykres porownujacy rozne etykiety (ustalone odgornie) 
    dla danych benchmarkowych dwuwymiarowych
    """
    fig, axs = plt.subplots(1, 2, figsize=(15,5))
    fig.tight_layout()
        
    axs[0].scatter(data[:,0], data[:,1], c=labels[0])
    axs[0].set_title("labels0")
        
    axs[1].scatter(data[:,0], data[:,1], c=labels[1])
    axs[1].set_title("labels1")
    
    _fig_name = file_name + "_two_labels" + ".png"
    _fig_path = os.path.join(path, _fig_name)
    fig.savefig(_fig_path, format='png', transparent=True,
                    bbox_inches='tight', dpi=150) 

    return


def wykres6(x,y,pred, titles, true_pred, file_name, path):
    """
    porównanie wyników algorytmów klasteryzacji na danym zbiorze w dwóch wymiarach
    """
    fig, axs = plt.subplots(2, 2, figsize=(10,10))
    fig.tight_layout()
    
    axs[0, 0].scatter(x, y, c=pred[-4])
    axs[0, 0].set_title(titles[-4])
    
    axs[0, 1].scatter(x, y, c=pred[-3])
    axs[0, 1].set_title(titles[-3])
    
    axs[1, 0].scatter(x, y, c=pred[-2])
    axs[1, 0].set_title(titles[-2])
    
    axs[1, 1].scatter(x, y, c=pred[-1])
    axs[1, 1].set_title(titles[-1])

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    _fig_name = file_name +'_'+  str(len(np.unique(true_pred))) + "_spectral_algorithm" + ".png"
    _fig_path = os.path.join(path, _fig_name)
    fig.savefig(_fig_path, format='png', transparent=True,
                    bbox_inches='tight', dpi=150) 
    
    return
        
    

names1 = ['K-means', 'AgglomerativeClustering - "ward" linkage', 
         'AgglomerativeClustering - "average" linkage', 
         'AgglomerativeClustering - "single" linkage',
         'AgglomerativeClustering - "complete" linkage', 
         'Genie algorithm', 'DBSCAN algorithm']

names2 = ['K-means', 'AgglomerativeClustering - "ward" linkage', 
         'AgglomerativeClustering - "average" linkage', 
         'AgglomerativeClustering - "single" linkage',
         'AgglomerativeClustering - "complete" linkage', 
         'Genie algorithm', 'DBSCAN algorithm', "Spectral algorithm M=1% of the points",
         "Spectral algorithm M=5% of the points", "Spectral algorithm M=10% of the points", 
          "Spectral algorithm M=30% of the points"]


def results_to_csv(path, file_name, spectral_algorithm, method_names, outfile_name=None, std=False):
    """
    

    Parameters
    ----------
    path : type: string, sciezka do pliku .gz 
        DESCRIPTION.
    file_name : type: string
        nazwa pliku zbioru plikow .gz, potrzebna do funkcji 'load_dataset' 
    spectral_algorithm : type: bool, True - jesli uzyta zostala wlasna implementacja
        algorytmu spektralnego (w pojedynczych przykladach nie zostala uzyta z powodu
        zbyt duzego rozmiaru danych)
    
    method_names: type: list of strings, uzyte metody klasteryzacji
    
    outfile_name: type: string, name of .csv file to be saved (default == file_name)
    std: type: bool, if true then we standarize columns of the dataset
   
    Funkcja zapisuje wyniki benchmarkowe z danego zbioru do pliku .csv
    """
    
    if outfile_name == None:
        outfile_name = file_name
    
    dataset = load_dataset(file_name, path)
    dataset_data = dataset.data
    
    if std == True:
        dataset_data = StandardScaler().fit_transform(dataset_data)
        
    # manualne parametry M w algorytmie spektralnym dla zbiorow 'engytime', 'spiral'    
    if file_name == "engytime":
        #z powodu duzego rozmiaru danych stosujemy algorytm spektralny tylko raz
        import sys
        print(sys.getrecursionlimit())
        sys.setrecursionlimit(6000)
        
        engy1_spectral_pred = spectral_clustering(dataset_data, 2, int(dataset_data.shape[0]*0.01))
        wykres_2d(dataset_data, engy1_spectral_pred, "engytime_spectral_1%_", path1)
        method_names.append("Spectral algorithm M=1% of the points")
        
    if file_name == "spiral":
        #ustawiamy manualnie paramater M=10 w algorytmie spektralnym (wtedy działa dobrze)
        spiral_spectral_man = spectral_clustering(dataset_data, 3, 10)
        wykres_2d(dataset_data, spiral_spectral_man, "spiral_spectral_10_", path1)
        method_names.append("Spectral algorithm M=10")

        
    for i in range(len(dataset.labels)):
        clusters = len(np.unique(dataset.labels[i]))
        dataset_ARI, dataset_FMI, dataset_preds = compare_methods(clusters, dataset_data, 
                                                                 dataset.labels[i], spectral_algorithm)
       
        if file_name == "engytime":
            engy1_spectral_ARI = adjusted_rand_score(dataset.labels[i], engy1_spectral_pred)
            engy1_spectral_FMI = fowlkes_mallows_score(dataset.labels[i], engy1_spectral_pred)    
            dataset_ARI.append(engy1_spectral_ARI)
            dataset_FMI.append(engy1_spectral_FMI)
            dataset_preds.append(engy1_spectral_pred)
        
        if file_name == "spiral":
            spiral_man_spectral_ARI = adjusted_rand_score(dataset.labels[i], spiral_spectral_man)
            spiral_man_spectral_FMI = fowlkes_mallows_score(dataset.labels[i], spiral_spectral_man)    
            dataset_ARI.append(spiral_man_spectral_ARI)
            dataset_FMI.append(spiral_man_spectral_FMI)
            dataset_preds.append(spiral_spectral_man)
            
        data_shape = [dataset_data.shape] * len(dataset_ARI)
        
        source = {
            "Method": method_names,
            "Fowlkes-Mallows index": dataset_FMI,
            "Adjusted Rand index": dataset_ARI,
            "Predictions": dataset_preds,
            "Shape": data_shape,
            "Number of clusters": [clusters]*len(dataset_ARI)}
        
        if dataset_data.shape[1] == 2:
            wykres_2d(dataset_data, dataset.labels[i], outfile_name, path)
            
            wykres2(dataset_data[:,0],dataset_data[:,1],
                    dataset_preds, names1, dataset.labels[i], outfile_name, path)
            
            if len(dataset.labels) == 2:
                wykres5(dataset_data, dataset.labels, outfile_name, path)
            
            if spectral_algorithm == True:
                wykres6(dataset_data[:,0],dataset_data[:,1],dataset_preds, 
                        names2, dataset.labels[i], outfile_name, path)
            
            
        elif dataset_data.shape[1] == 3:
            wykres_3d(dataset_data, dataset.labels[i], outfile_name, path)
            
            wykres3(dataset_data[:,0],dataset_data[:,1],dataset_data[:,2], 
                    dataset_preds, names1, dataset.labels[i], outfile_name, path)
            
            if spectral_algorithm == True:
                wykres4(dataset_data[:,0],dataset_data[:,1],dataset_data[:,2], 
                    dataset_preds, names2, dataset.labels[i], outfile_name, path)

    
        dataframe = pd.DataFrame.from_dict(source)
        if len(dataset.labels)>1 and len(np.unique(dataset.labels[0]))==len(np.unique(dataset.labels[1])):
            dataframe.to_csv(path+'\\'+outfile_name + str(clusters)+ "_v" + str(i) + ".csv", index=False, sep=';')
        else:
            dataframe.to_csv(path+'\\'+outfile_name + '_' + str(clusters) + ".csv", index=False, sep=';')
            
    return
    
#sciezka do plikow
path1 = r"C:\Users\patry\OneDrive\Pulpit\Zdalne pw\Python - PadPy\Projekt_23_dane_benchmarkowe"


######### wywolania funkcji dla zbiorow wlasnych #############
results_to_csv(path1, "zbior1", True, names2)
results_to_csv(path1, "zbior2", True, names2)
results_to_csv(path1, "zbior3", True, names2)
#standaryzacja
results_to_csv(path1, "zbior1", True, names2, outfile_name="zbior1_std", std=True)
results_to_csv(path1, "zbior2", True, names2, outfile_name="zbior2_std", std=True)
results_to_csv(path1, "zbior3", True, names2, outfile_name="zbior3_std", std=True)


######### wywolania funkcji dla pobranych zbiorow #############
results_to_csv(path1, "line", True, names2)   
results_to_csv(path1, "parabolic", True, names2)    
results_to_csv(path1, "spiral", True, names2.copy())
results_to_csv(path1, "engytime", False, names1.copy()) 
results_to_csv(path1, "zigzag_noisy", True, names2) 
results_to_csv(path1, "square", True, names2) 
results_to_csv(path1, "isolation", False, names1)
results_to_csv(path1, "chainlink", True, names2)
results_to_csv(path1, "atom", True, names2)
results_to_csv(path1, "sonar", True, names2)
#standaryzacja
results_to_csv(path1, "line", True, names2, outfile_name="line_std", std=True)
results_to_csv(path1, "parabolic", True, names2, outfile_name="parabolic_std", std=True)
results_to_csv(path1, "spiral", True, names2.copy(), outfile_name="spiral_std", std=True)
results_to_csv(path1, "zigzag_noisy", True, names2, 
               outfile_name="zigzag_noisy_std", std=True)
results_to_csv(path1, "square", True, names2, outfile_name="square_std", std=True)
results_to_csv(path1, "isolation", False, names1, outfile_name="isolation_std", std=True)
results_to_csv(path1, "chainlink", True, names2, outfile_name="chainlink_std", std=True)
results_to_csv(path1, "atom", True, names2, outfile_name="atom_std", std=True)
results_to_csv(path1, "sonar", True, names2, outfile_name="sonar_std", std=True)

