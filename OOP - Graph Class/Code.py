#------------------------Przetwarzanie danych w języku Python - Projekt 1-------------------------------------


class Graph:
    
    __slots__ = ['__edges', '__directed']
    def __init__(self, edges, directed):
        '''
        Parametry
        ----------
        edges : TYPE - list
        directed : TYPE - bool.

        Zakladamy, ze elementami parametru edges sa listy zawieracjace krawedzie przy danych wierzcholkach
        (ponumerowanych kolejno od 1 do len(edges))
        Przy czym zakladamy, ze dana krawedz pojawia sie tylko raz - w innym przypadku usuwamy powtarzajace sie
        krawedzie
        '''
        #poprawnosc typow argumentow
        if not(isinstance(edges, list)) or not(isinstance(directed, bool)):
            raise Exception("Incorrect type of arguments")
        
        for i in edges:
            if isinstance(i, list):
                if len(i)>0:
                    #sprawdzamy, czy elementy listy 'edges' to krotki + czy elementy krotek to int

                    if not(all(isinstance(j,tuple) for j in i)):
                        #niepoprawne typy elementow listy - krawedzie powinny byc w postaci krotek
                        raise Exception("Incorrect data type of neighbouring vertex or weight - it must be a tuple")
                
                for j in i:     
                    if j[0]>len(edges) or j[0]<=0:
                        raise Exception("The vertices with this number do not exist in the graph")
                    
                    if j[1]<=0:
                        raise Exception("The weight has to be a positive integer")
                        
                    for k in j:
                        if not(isinstance(k,int)):
                            raise Exception("The number of vertex or weight have to be integers!")
                
            else:
                #elementy listy nie sa krotkami
                raise Exception("Incorrect type of list elements")
            
        
        #sprawdzamy czy w grafie skierowanym nie występują krawędzie skierowane w obie strony 
        #lub czy w grafie nieskierowanym krawedzie sie nie powtarzaja/te same krawedzie nie maja roznych wag
        edges_sets = []
        edges_sets_with_weights = []
        for i in range(len(edges)):
            for j in edges[i]:
                if {i+1,j[0]} in edges_sets:
                    if directed == True:
                        raise Exception("Incorrect direction of the edges in the Graph")
                    else:
                        #usuwamy krawedz ktora sie powtarza
                        if [j[1],j[0],i+1] in edges_sets_with_weights:
                            edges[i].remove(j)
                        
                        #wagi krawedzi sie nie zgadzaja
                        else:
                            raise Exception("Different weights for the same edge in undirected graph")
                            
                else:
                    edges_sets.append({i+1,j[0]})
                    edges_sets_with_weights.append([j[1],i+1,j[0]])
            
        self.__edges = edges
        self.__directed = directed
        
    def __len__(self):
        return len(self.__edges)
    
    def get_edges(self):
        return self.__edges #dopytać
    
    def add_vertex(self):
        #funkcja dodaje jeden wierzcholek do grafu
        self.__edges.append([])
    
    def add_edge(self, v1, v2, value):
        '''
        Parametry
        ----------
        v1 : TYPE - integer (pierwszy wierzcholek)
        v2 : TYPE - integer (drugi wierzcholek)
        value : TYPE - integer (waga krawedzi)

        funkcja dodaje do parametru edges krawedz (do krawedzi przy wierzcholku v1 - 
        krawedz z wierzcholkiem v2 i waga 'value')
        '''
        
        if v1 > len(self.__edges) or v2 > len(self.__edges) or v1<=0 or v2<=0:
            raise Exception("The vertices with this number do not exist in the graph")
            
        if not(isinstance(v1,int) and isinstance(v2,int) and isinstance(value,int)):
            raise Exception("The number of vertex or weight have to be integers!")
        
        for i in self.__edges[v1-1]:    #sprawdzamy pierwsze elementy krotek dla krawędzi przy wierzchołku v1
            if v2 == i[0]:
                return "The specified edge is already in the graph"
            
        for i in self.__edges[v2-1]:    #sprawdzamy pierwsze elementy krotek dla krawędzi przy wierzchołku v2
                                        #(zgodnie zalozeniami nie powtarzamy krawedzi)
            if v1 == i[0]:
                return "The specified edge is already in the graph"
            
        self.__edges[v1-1].append((v2,value))
        return
    
    def to_adjacency_matrix(self):
        '''
        funkcja zwraca macierz sasiedztwa - kazdy wiersz reprezentuje wagi krawedzi dla danego wierzcholka
        (o numerze wiersza) z innymi wierzcholkami (o numerze kolumny)
        zerowe elementy macierzy oznaczaja, ze pomiedzy wierzcholkami o numerach wiersza i kolumny nie maja 
        wspolnej krawedzi
        '''
        matrix = [[0 for i in range(len(self.__edges))] for i in range(len(self.__edges))]
        
        for i in range(len(self.__edges)):
            for j in range(len(self.__edges[i])):
                matrix[i][self.__edges[i][j][0]-1] = self.__edges[i][j][1]
        
        return matrix
    
    def __str__(self):
        print_graph = ''
        
        if self.__directed == True:
            direct = 'Directed graph \n' + 'edges: \n'
                   
            for i in range(len(self.__edges)):
                for j in range(len(self.__edges[i])):
                    
                    if j < len(self.__edges[i])-1:
                        print_graph += str(i+1) + '--(' + str(self.__edges[i][j][1]) + \
                                   ')-->' + str(self.__edges[i][j][0]) + ',  '

                    else:
                        print_graph += str(i+1) + '--(' + str(self.__edges[i][j][1]) + \
                                   ')-->' + str(self.__edges[i][j][0]) + '\n'
                    
            
        else:
            direct = 'Undirected graph \n' + 'edges: \n'
            
            for i in range(len(self.__edges)):
                for j in range(len(self.__edges[i])):
                    
                    if j < len(self.__edges[i])-1:
                        print_graph += str(i+1) + '<--(' + str(self.__edges[i][j][1]) + \
                                   ')-->' + str(self.__edges[i][j][0]) + ',  '

                    else:
                        print_graph += str(i+1) + '<--(' + str(self.__edges[i][j][1]) + \
                                   ')-->' + str(self.__edges[i][j][0]) + '\n'
            
        return direct + print_graph
    
    def __repr__(self):
        return f"Graph(edges= {self._Graph__edges}, directed= {self._Graph__directed})"
    
    def Kruskal_tree(self):
        '''
        funkcja zwraca obiekt klasy Graph, ktory jest minimalnym drzewem rozpinajacym (znajdujemy je zgodnie
        z algorytmem Kruskala)
        funkcja wyrzuca blad dla grafow niespojnych
        '''
        
        from disjoint_set import DisjointSet
        if self.__directed == True:
            raise Exception("Graph must be undirected")
        
        #tworzymy graf wynikowy, poki co bez zadnych krawedzi 
        T = Graph([[] for i in range(len(self.__edges))], False)
        
        edges = []
        vertices = DisjointSet()
        
        #tworzymy liste krawedzi (z tym, ze teraz dla kazdej krawedzi mamy informacje o dwoch wierzcholkach 
        # + waga)
        #tworzymy liste ze zbiorami wierzcholkow
        for i in range(len(self.__edges)):
            vertices.find(i)
            
            for j in range(len(self.__edges[i])): 
                a = list(self.__edges[i][j]).copy()
                a.append(i+1)
                edges.append(a)
                #czyli mamy [wierzcholek2, waga, wierzcholek1] 
        
        edges.sort(key = lambda x: x[1]) #sortujemy niemalejaco po wagach
        
        vert_number = len(self.__edges)
        
        i=0
        while i < len(edges): 
            if vertices.connected(edges[i][0], edges[i][2]) == False:
                T.add_edge(edges[i][2], edges[i][0], edges[i][1])
                vertices.union(edges[i][0], edges[i][2])
                vert_number = vert_number - 1
            i += 1
            
            if vert_number == 1:
                break
        
        #wyrzucamy blad dla grafu niespojnego (czyli istnieja co najmniej 2 rozne podgafy spojne i juz nie ma
        # zadnej krawedzi pomiedzy nimi)
        if (i == len(edges)) and (vert_number>1):
            raise Exception("There is no minimal spanning tree for an inconsistent graph")
        
        return T



#-----------------------------------testy----------------------------------------------------

#--------test1------------        
e1 =  [ [(2, 3), 5, 5], [(3, 1), (4, 10), (5, 11)] ,[(4, 5)], [(5, 3)], []]      
test1 = Graph(e1,True)
#zwraca blad - krawedzie powinny byc w postaci krotek 


#--------test2------------ 
e2 =  [ [(2, 3), (5, 5)], [(3, 1), (4, 10), (5, 11)] ,[(4, 5)], [(5, 3)]]      
test2 = Graph(e2,True)      
#zwraca blad - krawedzie w postaci krotek odwoluja sie do wierzcholkow, ktorych nie ma w grafie 


#--------test3------------ 
e3 =  [ [(2, 3), (5, 5)], [(3, 1), (4, 10), (5, 11)] ,[(4, 5)], [(5, 3)], [(1,5)]]      
test3 = Graph(e3,True)
#zwraca blad - w grafie skierowanym krawedz w argumencie 'edges' moze wystapic tylko przy jednym wierzcholku
# (w tym, od ktorego jest skierowany)


#--------test4------------ 
e4 =  [ [(2, 3), (5, 5)], [(3, 1), (4, 10), (5, 11)] ,[(4, 5)], [(5, 3)], [(1,5)]]      
test4 = Graph(e4,False)
test4.get_edges()
# dla grafu skierowanego nie zwraca bledu, ale automatycznie duplikat krawedzi powtarzajacej sie
# (przy wierzcholku nr 5) jest usuwany


#--------test5------------ 
e5 =  [ [(2, 3), (5, 5)], [(3, 1), (4, 10), (5, 11)] ,[(4, 5)], [(5, 3)], [(1,20)]]
test5 = Graph(e5,False)
#zwraca blad - tutaj dla tej samej krawedzi w grafie nieskierowanym przypisane sa rozne wagi


#--------test6------------ 
e6 =  [ [(2, 3), (5, 0)], [(3, 1), (4, 10), (5, 11)] ,[(4, 5)], [(5, 3)], []]
test6 = Graph(e6,False)
#zwraca blad - wagi krawedzi musza byc calkowite dodatnie


#--------test7------------ 
#dzialanie roznych metod
test7 = Graph([[] for i in range(3)], False) #tworzymy pusty graf o 3 wierzcholkach
test7.get_edges()
test7.add_vertex() #dodajemy 4 wierzcholek
#dodajemy krawedzie
test7.add_edge(1, 2, 10)
test7.add_edge(1, 3, 6)
test7.add_edge(1, 4, 5)
test7.add_edge(2, 4, 15)
test7.add_edge(3, 4, 4)
print(test7) #reprezentacja grafu
repr(test7)
test7.get_edges()
T = test7.Kruskal_tree()     
print(T) #minimalne drzewo rozpinajace        
        

#--------test8------------ 
e8 = [[(2,10), (6,23)],
     [(3,15)],
     [(4,3)],
     [(5,17)],
     [(6,28)],
     [],
    [(1,1), (2,4), (3,9), (4,16), (5,25), (6,36)],
    [(9,4)],
    []]
test8 = Graph(e8, False)
print(test8)
T8 = test8.Kruskal_tree()
#Zwracany jest blad - graf jest niespojny, wiec dla takiego grafu nie mozemy znalezc 
# minimalnego drzewa rozpinajacego
