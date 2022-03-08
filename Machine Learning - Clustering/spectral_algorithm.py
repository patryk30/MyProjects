# -*- coding: utf-8 -*-
"""
implementacja algorytmu spektralnego
"""

#pakiety
import numpy as np
from sklearn.cluster import KMeans


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