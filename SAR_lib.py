import json
from nltk.stem.snowball import SnowballStemmer
import os
import re
import math


class SAR_Project:
    """
    Prototipo de la clase para realizar la indexacion y la recuperacion de noticias
        
        Preparada para todas las ampliaciones:
          parentesis + multiples indices + posicionales + stemming + permuterm + ranking de resultado
    Se deben completar los metodos que se indica.
    Se pueden añadir nuevas variables y nuevos metodos
    Los metodos que se añadan se deberan documentar en el codigo y explicar en la memoria.Modificación
    """

    # lista de campos, el booleano indica si se debe tokenizar el campo
    # NECESARIO PARA LA AMPLIACION MULTIFIELD
    fields = [("title", True), ("date", False),
              ("keywords", True), ("article", True),
              ("summary", True)]
    
    
    # numero maximo de documento a mostrar cuando self.show_all es False
    SHOW_MAX = 10


    def __init__(self):
        """
        Constructor de la classe SAR_Indexer.
        NECESARIO PARA LA VERSION MINIMA
        Incluye todas las variables necesaria para todas las ampliaciones.
        Puedes añadir más variables si las necesitas 
        """
        self.index = {
                'title': {},
                'date': {},
                'keywords': {},
                'summary': {},
                'article': {}
        } # hash para el indice invertido de terminos --> clave: termino, valor: posting list.
                        # Si se hace la implementacion multifield, se pude hacer un segundo nivel de hashing de tal forma que:
                        # self.index['title'] seria el indice invertido del campo 'title'.
        self.sindex = {
                'title': {},
                'date': {},
                'keywords': {},
                'summary': {},
                'article': {}
        } # hash para el indice invertido de stems --> clave: stem, valor: lista con los terminos que tienen ese stem
        self.ptindex = {
                'title': {},
                'date': {},
                'keywords': {},
                'summary': {},
                'article': {}
        } # hash para el indice permuterm.
        self.docs = {} # diccionario de terminos --> clave: entero(docid),  valor: ruta del fichero.
        self.weight = {} # hash de terminos para el pesado, ranking de resultados. puede no utilizarse
        self.news = {} # hash de noticias --> clave entero (newid), valor: la info necesaria para diferencia la noticia dentro de su fichero
        self.tokenizer = re.compile("\W+") # expresion regular para hacer la tokenizacion
        self.stemmer = SnowballStemmer('spanish') # stemmer en castellano
        self.show_all = False # valor por defecto, se cambia con self.set_showall()
        self.show_snippet = False # valor por defecto, se cambia con self.set_snippet()
        self.use_stemming = False # valor por defecto, se cambia con self.set_stemming()
        self.use_ranking = False  # valor por defecto, se cambia con self.set_ranking()

    ###############################
    ###                         ###
    ###      CONFIGURACION      ###
    ###                         ###
    ###############################

    ############
    ### Prueba##
    ############


        self.docid = 0
        self.newid = 0

        # Days counter
        self.num_days = {}
        self.term_frequency = {}
        # Searched terms in the query
        self.searched_terms = []

    def set_showall(self, v):
        """
        Cambia el modo de mostrar los resultados.
        
        input: "v" booleano.
        UTIL PARA TODAS LAS VERSIONES
        si self.show_all es True se mostraran todos los resultados el lugar de un maximo de self.SHOW_MAX, no aplicable a la opcion -C
        """
        self.show_all = v


    def set_snippet(self, v):
        """
        Cambia el modo de mostrar snippet.
        
        input: "v" booleano.
        UTIL PARA TODAS LAS VERSIONES
        si self.show_snippet es True se mostrara un snippet de cada noticia, no aplicable a la opcion -C
        """
        self.show_snippet = v


    def set_stemming(self, v):
        """
        Cambia el modo de stemming por defecto.
        
        input: "v" booleano.
        UTIL PARA LA VERSION CON STEMMING
        si self.use_stemming es True las consultas se resolveran aplicando stemming por defecto.
        """
        self.use_stemming = v


    def set_ranking(self, v):
        """
        Cambia el modo de ranking por defecto.
        
        input: "v" booleano.
        UTIL PARA LA VERSION CON RANKING DE NOTICIAS
        si self.use_ranking es True las consultas se mostraran ordenadas, no aplicable a la opcion -C
        """
        self.use_ranking = v




    ###############################
    ###                         ###
    ###   PARTE 1: INDEXACION   ###
    ###                         ###
    ###############################


    def index_dir(self, root, **args):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        
        Recorre recursivamente el directorio "root"  y indexa su contenido
        los argumentos adicionales "**args" solo son necesarios para las funcionalidades ampliadas
        """
        self.multifield = args['multifield']
        self.positional = args['positional']
        self.stemming = args['stem']
        self.permuterm = args['permuterm']

        for d, subdirs, files in os.walk(root):
            for filename in files:
                if filename.endswith('.json'):
                    fullname = os.path.join(d, filename)
                    self.index_file(fullname)

        ##########################################
        ## COMPLETAR PARA FUNCIONALIDADES EXTRA ##
        ##########################################
        

    def index_file(self, filename):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Indexa el contenido de un fichero.
        Para tokenizar la noticia se debe llamar a "self.tokenize"
        Dependiendo del valor de "self.multifield" y "self.positional" se debe ampliar el indexado.
        En estos casos, se recomienda crear nuevos metodos para hacer mas sencilla la implementacion
        input: "filename" es el nombre de un fichero en formato JSON Arrays (https://www.w3schools.com/js/js_json_arrays.asp).
                Una vez parseado con json.load tendremos una lista de diccionarios, cada diccionario se corresponde a una noticia
        """

        with open(filename, encoding='utf-8') as fh:
            jlist = json.load(fh)

        #
        # "jlist" es una lista con tantos elementos como noticias hay en el fichero,
        # cada noticia es un diccionario con los campos:
        #      "title", "date", "keywords", "article", "summary"
        #
        # En la version basica solo se debe indexar el contenido "article"
        #
        #
        #
        #################
        ### COMPLETAR ###
        #################
        self.docs[self.docid] = filename
        if self.positional:
            for new in jlist:
                for field in self.fields:
                    #print(field[0])
                    #if field[1]:
                    nTokens = self.tokenize(new[field[0]]) #if self.fields['article'] else [] #new["article"])

                    nt = 0
                    for token in nTokens:
                        if not self.index[field[0]].get(token, 0):
                            self.index[field[0]][token] = {}
                        if  not self.index[field[0]][token].get((self.docid, self.newid),0):
                            self.index[field[0]][token][(self.docid, self.newid)] = []
                        if (self.docid, self.newid) in self.index[field[0]][token]:
                            self.index[field[0]][token][(self.docid, self.newid)].append(nt)
                           
                        nt = nt + 1     

                        # frecuencia de las palabras
                        if self.weight.get(token) == None:
                            self.weight[token] = {self.newid: 0}
                        self.weight[token][self.newid] = 1 if self.weight[token].get(self.newid) == None else self.weight[token][self.newid] + 1
                self.news[self.newid] = (self.docid, new["date"], new["title"], new["keywords"], nt)
                self.newid += 1
                
                # COunters for TOKENS
                self.num_days[new['date']] = 1 if self.num_days.get(new['date']) == None else self.num_days[new['date']] + 1# Days counter

        else:
            for new in jlist:
                    for field in self.fields:
                        #print(field[0])
                        if field[1]:
                            nTokens = self.tokenize(new[field[0]]) #if self.fields['article'] else [] #new["article"])
                            nt = 0
                            for token in nTokens:
                                if not self.index[field[0]].get(token, 0):
                                    self.index[field[0]][token] = {}
                                if (self.docid, self.newid) not in self.index[field[0]][token]:
                                    self.index[field[0]][token][(self.docid, self.newid)] = []
                                nt = nt + 1    
                                
                                # frecuencia de las palabras
                                if self.weight.get(token) == None:
                                    self.weight[token] = {self.newid: 0}
                                self.weight[token][self.newid] = 1 if self.weight[token].get(self.newid) == None else self.weight[token][self.newid] + 1
                        else:
                            nt = 0
                            token = new[field[0]]

                            if not self.index[field[0]].get(token, 0):
                                    self.index[field[0]][token] = {}
                            if (self.docid, self.newid) not in self.index[field[0]][token]:
                                self.index[field[0]][token][(self.docid, self.newid)] = []
                            nt = nt + 1    
                    
                    self.news[self.newid] = (self.docid, new["date"], new["title"], new["keywords"], nt)
                    self.newid += 1
                    # COunters for TOKENS
                    self.num_days[new['date']] = 1 if self.num_days.get(new['date']) == None else self.num_days[new['date']] + 1# Days counter
                    # COunters for TOKENS
                    #self.num_days[new['date']] = True # Days counter
        self.docid = self.docid + 1




    def tokenize(self, text):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Tokeniza la cadena "texto" eliminando simbolos no alfanumericos y dividientola por espacios.
        Puedes utilizar la expresion regular 'self.tokenizer'.
        params: 'text': texto a tokenizar
        return: lista de tokens
        """
        return self.tokenizer.sub(' ', text.lower()).split()



    def make_stemming(self):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING.
        Crea el indice de stemming (self.sindex) para los terminos de todos los indices.
        self.stemmer.stem(token) devuelve el stem del token
        """
        
        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################
        # Searching for the different fields
        f = []
        for i in self.fields:
            f.append(i[0])

        for field in f:
            for termino in self.index[field].keys():
                term = self.stemmer.stem(termino)
                if self.sindex[field].get(term) == None:
                    self.sindex[field][term] = [termino]
                else:
                    self.sindex[field][term] = self.sindex[field][term] + [termino]


    
    def make_permuterm(self):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM
        Crea el indice permuterm (self.ptindex) para los terminos de todos los indices.
        
        > self.ptindex[field][term]
        """
        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################
        
        if self.multifield:
            # Searching for the different fields
            f = []
            for i in self.fields:
                f.append(i[0])

            for field in range(len(f)):
                for termino in self.index[f[field]].keys():
                    t = termino
                    termino += '$'
                    permutations = []

                    for i in range(len(termino)):
                        termino = termino[1:] + termino[0]
                        permutations.append(termino)
                    #self.ptindex[f[field]][t] = len(permutations) if self.ptindex[f[field]].get(t) == None else self.ptindex[f[field]][t] + len(permutations)
                    if self.ptindex[f[field]].get(t) == None:
                        self.ptindex[f[field]][t] = permutations
                    else:
                        self.ptindex[f[field]][t] = self.ptindex[f[field]][t] + permutations
        else:
            for termino in self.index['article'].keys():
                termino += '$'
                permutations = []

                for i in range(len(termino)):
                    termino = termino[1:] + termino[0]
                    permutations = permutations + [termino]

                #self.ptindex['article'][termino] = len(permutations)
                #self.ptindex['article'][termino] = permutations if self.ptindex['article'].get(termino) == None else self.ptindex['article'][termino] + termino 
                if self.ptindex['article'].get(termino) == None:
                    self.ptindex['article'][termino] = permutations
                else:
                    self.ptindex['article'][termino] = self.ptindex['article'][termino] + permutations


    def show_stats(self):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        
        Muestra estadisticas de los indices
        
        """
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################

        print("=" * 40)
        print("Number of indexed days: " + str(len(self.num_days)))
        print("-" * 40)
        print("Number of indexed news: " + str(len(self.news)))
        print("-" * 40)
        print("TOKENS:")

        # Searching for the different fields
        f = []
        for i in self.fields:
            f.append(i[0])
        # ------------------------------- If multified option is active ----------------------
        if self.multifield:
            print("\t# of tokens in \'title\': " + str(len(self.index['title'])))
            print("\t# of tokens in \'date\': " + str(len(self.num_days)))#len(self.index['date'])))
            print("\t# of tokens in \'keywords\': " + str(len(self.index['keywords'])))
            print("\t# of tokens in \'article\': " + str(len(self.index['article'])))
            print("\t# of tokens in \'summary\': " + str(len(self.index['summary'])))
            print("-" * 40)

        # ------------------------------- If permuterm option is active ----------------------
        if self.permuterm:
            print("PERMUTERMS:")
            # Making permuterms 
            self.make_permuterm()
            for field in f:
                i = 0
                if field == 'date':
                    for t in self.num_days.keys():
                        i += len(t) + 1
                    print("\t# of tokens in \'",field,"\': " + str(i))
                else:
                    for term in self.ptindex[field].keys():
                        i += len(self.ptindex[field][term])
                    print("\t# of tokens in \'",field,"\': " + str(i))
            print("-" * 40)

        if self.stemming:
            print("STEMS:")
            # Making permuterms 
            self.make_stemming()

            # Counting the different fields
            #for field in f:
            #    print("\t# of tokens in \'",field,"\': " + str(len(self.sindex[field].keys())))
            print("\t# of tokens in \'title\': " + str(len(self.sindex['title'].keys())))
            print("\t# of tokens in \'date\': " + str(len(self.num_days)))
            print("\t# of tokens in \'keywords\': " + str(len(self.sindex['keywords'].keys())))
            print("\t# of tokens in \'article\': " + str(len(self.sindex['article'].keys())))
            print("\t# of tokens in \'summary\': " + str(len(self.sindex['summary'].keys())))
            print("-" * 40)

        else:
            print("\t# of tokens in \'article\': " + str(len(self.index['article'])))
        if self.positional:
            print("Positional queries are alowed.")
        else:
            print("Positional queries are NOT alowed.")
        print("=" * 40)



    ###################################
    ###                             ###
    ###   PARTE 2.1: RECUPERACION   ###
    ###                             ###
    ###################################


    def solve_query(self, query, prev={}):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Resuelve una query.
        Debe realizar el parsing de consulta que sera mas o menos complicado en funcion de la ampliacion que se implementen
        param:  "query": cadena con la query
                "prev": incluido por si se quiere hacer una version recursiva. No es necesario utilizarlo.
        return: posting list con el resultado de la query
        """

        if query is None or len(query) == 0:
            return []

        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################
        result = []
        self.searched_terms = []
        if '\"' in query:
            query = query.replace('\"' ,' \" ' )
            #P.eje pasar de "h" a " h "
        qParts = query.split()

        aux = 0

        while aux < len(qParts):
        	if qParts[aux] != "AND" and qParts[aux] != "NOT" and qParts[aux] != "OR":
        		qParts[aux] = qParts[aux].lower()
        	aux = aux + 1

        i = 0
        if qParts[i] == "AND" or qParts[i] == "OR":
            return result
        if len(qParts) < 3:
            if len(qParts) == 2 and qParts[i] == "NOT":
                if ':' in qParts[1]:
                    mqParts = qParts[1].split(':')
                    nextP = self.get_posting(mqParts[1], mqParts[0])
                else:
                    nextP = self.get_posting(qParts[1])
                nextP = list(nextP)
                nextP.sort()
                return self.reverse_posting(nextP)
            elif len(qParts) <= 2  and qParts[i] != "NOT":
                if ':' in qParts[i]:
                    mqParts = qParts[i].split(':')
                    nextP = self.get_posting(mqParts[1], mqParts[0])
                if '*' in qParts[i] or '?' in qParts[i]:
                    nextP = self.get_permuterm(qParts[i])
                    
                else:
                    nextP = self.get_posting(qParts[i])

                nextP = list(nextP)
                nextP.sort()
                return nextP
            else:

                return result
        else:
            while i < len(qParts) - 1:

                if qParts[i] == "\"":
                    newQP = qParts
                    newQP = newQP[1:]
                    pos = newQP.index("\"") + 1
                    newQP = qParts[1:pos]
                    result = self.get_positionals(newQP)
                    i = i + pos + 1
                else:
                    if qParts[i] == "NOT":
                        if qParts[i + 1] == "\"":
                            newQP = qParts
                            pos = newQP.index("\"") + 1
                            newQP = qParts[i+2:pos+i+2]
                            nextP = self.get_positionals(newQP)
                            nextP = list(nextP)
                            nextP.sort()
                            result = self.and_posting(result, nextP)
                            i = i + pos + 1
                        if ':' in qParts[i + 1]:
                            mqParts = qParts[i + 1].split(':')
                            nextP = self.get_posting(mqParts[1], mqParts[0])
                        else:
                            nextP = self.get_posting(qParts[i + 1])
                        nextP = list(nextP)
                        nextP.sort()
                        result = self.reverse_posting(nextP)
                        i = i + 1
                    else:
                        if qParts[i] == "AND":                               
                            if qParts[i + 1] == "\"":

                                    newQP = qParts

                                    pos = newQP.index("\"") + 1

                                    newQP = qParts[i+2:pos+i+2]

                                    nextP = self.get_positionals(newQP)
                                    nextP = list(nextP)

                                    nextP.sort()

                                    result = self.and_posting(result, nextP)

                                    i = i + pos + 1
                            elif qParts[i + 1] == "NOT":
                                if qParts[i + 2] == "\"":
                                    newQP = qParts
                                    pos = newQP.index("\"") + 1
                                    newQP = qParts[i+3:pos+i+3]
                                    nextP = self.get_positionals(newQP)
                                    nextP = list(nextP)
                                    nextP.sort()
                                    result = self.and_posting(result, nextP)
                                    i = i + pos + 2
                                elif ':' in qParts[i + 2]:
                                    mqParts = qParts[i + 2].split(':')
                                    nextP = self.get_posting(mqParts[1], mqParts[0])
                                    if qParts[i + 1] == "\"":
                                        newQP = qParts
                                        newQP = newQP[1:]
                                        pos = newQP.index("\"") + 1
                                        newQP = qParts[1:pos]
                                        result = self.get_positionals(newQP)
                                        i = i + pos
                                else:
                                    nextP = self.get_posting(qParts[i + 2])
                                nextP = list(nextP)
                                nextP.sort()
                                nextP = self.reverse_posting(nextP)
                                result = self.and_posting(result, nextP)
                                i = i + 2
                            else:

                                if ':' in qParts[i + 1]:
                                    mqParts = qParts[i + 1].split(':')
                                    nextP = self.get_posting(mqParts[1], mqParts[0])

                                else:
                                    nextP = self.get_posting(qParts[i + 1])
                                nextP = list(nextP)
                                nextP.sort()
                                result = self.and_posting(result, nextP)
                                i = i + 1
                        elif qParts[i] == "OR":
                            if qParts[i + 1] == "\"":
                                    newQP = qParts
                                    pos = newQP.index("\"") + 1
                                    newQP = qParts[i+2:pos+i+2]
                                    nextP = self.get_positionals(newQP)
                                    nextP = list(nextP)
                                    nextP.sort()
                                    result = self.and_posting(result, nextP)
                                    i = i + pos + 1
                            elif qParts[i + 1] == "NOT":
                                if qParts[i + 2] == "\"":
                                    newQP = qParts
                                    pos = newQP.index("\"") + 2
                                    newQP = qParts[i+3:pos+i+3]
                                    nextP = self.get_positionals(newQP)
                                    nextP = list(nextP)
                                    nextP.sort()
                                    result = self.and_posting(result, nextP)
                                    i = i + pos + 2
                                elif ':' in qParts[i + 2]:
                                    mqParts = qParts[i + 2].split(':')
                                    nextP = self.get_posting(mqParts[1], mqParts[0])
                                else:
                                    nextP = self.get_posting(qParts[i + 2])
                                nextP = list(nextP)
                                nextP.sort()
                                nextP = self.reverse_posting(nextP)
                                result = self.or_posting(result, nextP)
                                i = i + 2
                            else:
                                if ':' in qParts[i + 1]:
                                    mqParts = qParts[i + 1].split(':')
                                    nextP = self.get_posting(mqParts[1], mqParts[0])
                                else:
                                    nextP = self.get_posting(qParts[i + 1])
                                nextP = list(nextP)
                                nextP.sort()
                                result = self.or_posting(result, nextP)
                                i = i + 1
                        else:
                            if ':' in qParts[i]:
                                mqParts = qParts[i].split(':')
                                result = self.get_posting(mqParts[1], mqParts[0])
                            else:
                                result = self.get_posting(qParts[i])
                            result = list(result)
                            result.sort()
                    i = i + 1
            
            return result


 


    def get_posting(self, term, field='article'):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Devuelve la posting list asociada a un termino. 
        Dependiendo de las ampliaciones implementadas "get_posting" puede llamar a:
            - self.get_positionals: para la ampliacion de posicionales
            - self.get_permuterm: para la ampliacion de permuterms
            - self.get_stemming: para la amplaicion de stemming
        param:  "term": termino del que se debe recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices
        return: posting list
        """
        
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################
        

        # NO me lo toqueis, es mio
        #return self.index[term]

        self.searched_terms.append(field + ":" + term)
        return self.index[field].get(term, [])



    def get_positionals(self, terms, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE POSICIONALES
        Devuelve la posting list asociada a una secuencia de terminos consecutivos.
        param:  "terms": lista con los terminos consecutivos para recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices
        return: posting list
        """
        
        ########################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE POSICIONALES ##
        ########################################################
        result = []

        diccionario_result = {}
        inicial = self.get_posting(terms[0])
        if len(terms) == 1:
            return inicial
        i = 1
        while i < len(terms):
            diccionario_result = {}
            lista_inicial = list(inicial)
            desp = self.get_posting(terms[i])
            lista_desp = list(desp)
            and_pos_list = self.and_posting(lista_inicial,lista_desp)
            for x in and_pos_list:
                lista_posicion_inicial = inicial[x]
                lista_posicion_desp = desp[x]
                j = 0
                k = 0
                while (j < len(lista_posicion_inicial)) & (k < len(lista_posicion_desp)):

                    if lista_posicion_inicial[j] == lista_posicion_desp[k] - 1:
                        if  not diccionario_result.get(x,0):
                            diccionario_result[x] = []
                        if x in diccionario_result:
                            ##Almacenamos en diicionario la posición del último elemento
                            diccionario_result[x].append(lista_posicion_desp[k])
                            

                        j = j + 1
                        k = k + 1
                    elif lista_posicion_inicial[j] < lista_posicion_desp[k] - 1:
                        j = j + 1
                    else:
                        k = k + 1
            inicial = diccionario_result
            i=i+1

        
        return list(diccionario_result)


    def get_stemming(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING
        Devuelve la posting list asociada al stem de un termino.
        param:  "term": termino para recuperar la posting list de su stem.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices
        return: posting list
        """
        
        stem = self.stemmer.stem(term)
        return self.sindex[field].get(stem, [])
        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################


    def get_permuterm(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM
        Devuelve la posting list asociada a un termino utilizando el indice permuterm.
        param:  "term": termino para recuperar la posting list, "term" incluye un comodin (* o ?).
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices
        return: posting list
        """
        ##################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA PERMUTERM ##
        ##################################################
        # Firstly we need to make the permuterm because of new files could be added
        self.make_permuterm()        


        resultado = []
        # Now we will search for all the words that can be associated with the given term
        term = term.replace("?", "*")
        query = term + '$'
        while query[-1] is not "*":
            query = query[1:] + query[0]
        print(query)
        print(query[:-1])
        # Searching for word, N squared O cost, but for this example is good due to 
        # optimization is not needed
        '''for permuterms in self.ptindex:
            for t in permuterms:
                if t.startswith(query[:-1]):
                    print("Permuterm encontrado")
                    return self.index[field][t]
                    #self.term_frequency[field][t]
        '''
        for perm in self.ptindex[field].keys():
            for t in self.ptindex[field][perm]:
                    if query[:-1] in t:

                        resultado = resultado + [t]
                    #self.term_frequency[field][t]
        print(resultado)
        return resultado




    def reverse_posting(self, p):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Devuelve una posting list con todas las noticias excepto las contenidas en p.
        Util para resolver las queries con NOT.
        param:  "p": posting list
        return: posting list con todos los newid exceptos los contenidos en p
        """

        
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################

        allnews = []
        newids = list(self.news.keys())
        newids.sort()
        for new in newids:
            allnews.append((self.news[new][0], new))
        result = []
        i = 0
        j = 0
        while (i < len(p)) & (j < len(allnews)):
            if p[i] == allnews[j]:
                i = i + 1
                j = j + 1
            elif p[i] < allnews[j]:
                i = i + 1
            else:
                result.append(allnews[j])
                j = j + 1
        
        while j < len(allnews):
            result.append(allnews[j])
            j = j + 1

        return result


    def and_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Calcula el AND de dos posting list de forma EFICIENTE
        param:  "p1", "p2": posting lists sobre las que calcular
        return: posting list con los newid incluidos en p1 y p2
        """
        
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################
        result = []
        i = 0
        j = 0
        while (i < len(p1)) & (j < len(p2)):
            if p1[i] == p2[j]:
                result.append(p2[j])
                i = i + 1
                j = j + 1
            elif p1[i] < p2[j]:
                i = i + 1
            else:
                j = j + 1

        return result



    def or_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Calcula el OR de dos posting list de forma EFICIENTE
        param:  "p1", "p2": posting lists sobre las que calcular
        return: posting list con los newid incluidos de p1 o p2
        """

        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################

        result = []
        i = 0
        j = 0
        while (i < len(p1)) & (j < len(p2)):
            if p1[i] == p2[j]:
                result.append(p2[j])
                i = i + 1
                j = j + 1
            elif p1[i] < p2[j]:
                result.append(p1[i])
                i = i + 1
            else:
                result.append(p2[j])
                j = j + 1
        
        while i < len(p1):
            result.append(p1[i])
            i = i + 1

        while j < len(p2):
            result.append(p2[j])
            j = j + 1

        return result


    def minus_posting(self, p1, p2):
        """
        OPCIONAL PARA TODAS LAS VERSIONES
        Calcula el except de dos posting list de forma EFICIENTE.
        Esta funcion se propone por si os es util, no es necesario utilizarla.
        param:  "p1", "p2": posting lists sobre las que calcular
        return: posting list con los newid incluidos de p1 y no en p2
        """
        ########################################################
        ## COMPLETAR PARA TODAS LAS VERSIONES SI ES NECESARIO ##
        ########################################################
        '''result = []
        i = 0
        j = 0
        while i < len(p1) & j < len(p2):
            pass'''
        pass





    #####################################
    ###                               ###
    ### PARTE 2.2: MOSTRAR RESULTADOS ###
    ###                               ###
    #####################################


    def solve_and_count(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Resuelve una consulta y la muestra junto al numero de resultados 
        param:  "query": query que se debe resolver.
        return: el numero de noticias recuperadas, para la opcion -T
        """
        result = self.solve_query(query)
        print("%s\t%d" % (query, len(result)))
        return len(result)  # para verificar los resultados (op: -T)


    def solve_and_show(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Resuelve una consulta y la muestra informacion de las noticias recuperadas.
        Consideraciones:
        - En funcion del valor de "self.show_snippet" se mostrara una informacion u otra.
        - Si se implementa la opcion de ranking y en funcion del valor de self.use_ranking debera llamar a self.rank_result
        param:  "query": query que se debe resolver.
        return: el numero de noticias recuperadas, para la opcion -T
        
        """
        result = self.solve_query(query)
        if self.use_ranking:
            result = self.rank_result(result, query)   

        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################

        print("=" * 40) 
        print("Query: " + query)
        print("Number of results: " + str(len(result)))
        nr = 1
        for r in result:
            new = self.news[r[1]]
            if not self.show_snippet:
                print("#" + str(nr) + "\t(0) (" + str(r[1]) + ") (" + str(new[1]) + ") " + str(new[2]) + " (" + str(new[3]) + ")")
            else:
                print("#" + str(nr))
                print("Score: " + str(0))
                print(str(r[1]))
                print("Date: " + str(new[1]))
                print("Title: " + str(new[2]))
                print("Keywords: " + str(new[3]))
                self.print_snippets(self.searched_terms,r[0],r[1],15)

            nr = nr + 1
            if nr > 100 and not self.show_all:
                break
            elif nr <= len(result):
                print("-" * 40)
        
        print("=" * 40)


    def print_snippets(self, terms, docid, newid, size):
        """
        Dados un documento y una noticia, imprime por cada término proporcionado 
        el primer snippet que lo contiene.
        param:  "terms": lista de terminos de los cuales queremos encontrar un snippet. Si el termino es de la forma "field:term" se buscará el el campo "field" de la noticia. Si no, se buscará en el artículo.
                "docid": id del documento que contiene la noticia en la que queremos buscar los snippets.
                "newid": id de la noticia en la cual queremos buscar los snippets.
                "size":  longitud máxima en palabras de los snippets que se mostrarán.
        return: el numero de noticias recuperadas, para la opcion -T
        """
        path = self.docs[docid]
        myNew = self.news[newid]
        targetNew = None
        with open(path) as fh:
            jlist = json.load(fh)
            for new in jlist:
                if (new["title"] == myNew[2]) & (new["date"] == myNew[1]):
                    targetNew = new
                    break
            
            for term in terms:
                field = "article"
                if ':' in term:
                    field = term.split(':')[0]
                    term = term.split(':')[1]
                tokens = self.tokenize(targetNew[field])
                pos = -1
                for i,token in enumerate(tokens):
                    if token == term:
                        pos = i
                        break
                snip = "... "
                if pos >= 0:
                    for j in range(max((pos - int(size/2) + 1), 0), min(pos + int(size/2), len(tokens) - 1)):
                        snip = snip + tokens[j] + " "
                    snip = snip + "..."
                    print(snip)




    def rank_result(self, result, query):
        """
        NECESARIO PARA LA AMPLIACION DE RANKING
        Ordena los resultados de una query.
        param:  "result": lista de resultados sin ordenar (id, posting)
                "query": query, puede ser la query original, la query procesada o una lista de terminos
        return: la lista de resultados ordenada     
        """

        # =================================== TRATAMIENTO DE RESULTS ===================================

        # Query preprocessing, Obtenemos las palabras positivas y negativas
        # ======================================================================================
        query = query.replace("(","")
        query = query.replace(")","")
        q = query.split()

        positiveQuery = []
        negativeQuery = []
        nop = ['AND', 'OR', 'NOT']
        
        for t in range(len(q)):
            if q[t] == 'NOT' and (t + 1) < len(q):
                negativeQuery.append(q[t + 1])
            
            elif q[t] not in nop and q[t] not in negativeQuery:
                positiveQuery.append(q[t])
        
        # ======================================================================================
        #   Preparativos para la distancia coseno
        # ======================================================================================
        
        consulta = {
            'ftq':{},
            'freq':{},
            'df':{},
            'tf':{},
            'idf':{},
            'wtd':{},
        }


        # Frecuencia de los terminos comunes, que serán sobre los que operaremos
        documento = {}   
        w = {}
        tftd = {
            'consulta':{},
            'doc':{}
        }

        df = {
            'consulta':{},
            'doc':{}
        }

        idf = {
            'consulta':{},
            'doc':{}
        }

        if len(result) > 0:
            for (r1, r2) in result:
                    w[(r1, r2)] = {}
                    documento[(r1, r2)] = {}
                    for p in positiveQuery + negativeQuery:
                            # ftd
                            documento[(r1, r2)][p] = self.weight[p][r2] # ftd

                            # tftd
                            tftd['doc'][p] = (1 + math.log(documento[(r1, r2)][p],10)) if documento[(r1, r2)].get(p) > 0 else 0
                            
                            # df
                            df['doc'][p] = len(self.weight[p].keys())

                            # idf
                            idf['doc'][p] = math.log((len(self.docs)) / df['doc'][p],10) if df['doc'][p] > 0 else 0 

                            # w
                            w[(r1,r2)][p] = tftd['doc'][p] * idf['doc'][p]

        # Normalizado
        for (r1, r2) in result:
            wNorm = {}
            media = 0.0
            for k in w[(r1,r2)].keys():
                media += w[(r1,r2)][k]**2
            media = media**0.5

            for p in w[(r1,r2)].keys():
                w[(r1,r2)][p] = w[(r1,r2)][p] / media
        #print(documento)
        #print("TFTD:", tftd)
        #print("DF:",df)
        #print("IDF:", idf)
        #print("W:", w)
        '''
            Como la Query siempre tendrá una palabra de cada, por lo tanto la frecuencia de las palabras de las query
            siempre seran una unidad, asi pues, obtenemos las palabras dichas en el result, y ahora calcularemos en el
            result los porcentajes y ordenadoremos en base a esto :)
        '''
        ranking = {}

        for (r1, r2) in result:
            r = 0
            for p in positiveQuery:
                r += abs(w[(r1,r2)][p])
            for p in negativeQuery:
                r -= abs(w[(r1,r2)][p])
            ranking[round(r,3)] = [(r1,r2)] if ranking.get(round(r,3)) == None else ranking[round(r,3)] + [(r1,r2)]

        # Obtengo los rankings ordenados
        result = []
        claves = list(ranking.keys())
        
        while len(claves) > 0:
            mayor = max(claves)
            result.append(ranking[mayor][0])
            claves.pop(claves.index(mayor))


        return result
        ###################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE RANKING ##
        ###################################################
