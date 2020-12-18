import re

from trie import Trie
from distancias_mejoradas import Distances

class SpellSuggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self, vocab_file_path):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que además se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """

        self.vocabulary  = self.build_vocab(vocab_file_path, tokenizer=re.compile("\W+"))

    def build_vocab(self, vocab_file_path, tokenizer):
        """Método para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        with open(vocab_file_path, "r", encoding='utf-8') as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard('') # por si acaso
            return sorted(vocab)

    def suggest(self, term, distance="levenshtein", threshold=None):

        """Método para sugerir palabras similares siguiendo la tarea 3.

        A completar.

        Args:
            term (str): término de búsqueda.
            distance (str): algoritmo de búsqueda a utilizar
                {"levenshtein", "restricted", "intermediate"}.
            threshold (int): threshold para limitar la búsqueda
                puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                o filtrando la salida de las distancias de la tarea 2
        """
        assert distance in ["levenshtein", "restricted", "intermediate"]

        results = {} # diccionario termino:distancia
        distanceFunc = None
        if distance == "levenshtein":
            distanceFunc = Distances.levenshtein
        elif distance == "restricted":
            distanceFunc = Distances.damerau_levenshtein_restringida
        else:
            distanceFunc = Distances.damerau_levenshtein_intermedia
        
        for word in self.vocabulary:
            if threshold == None:
                results[word] = int(distanceFunc(term, word))
            else:
                if len(word) <= len(term) + threshold:
                    d = distanceFunc(term, word, threshold)
                    if d != None and d <= threshold:
                        results[word] = int(d)
        
        return results
        
    def changeVocabulary(self, new_vocabulary):
        self.vocabulary = new_vocabulary

class TrieSpellSuggester(SpellSuggester):
    """
    Clase que implementa el método suggest para la búsqueda de términos y añade el trie
    """
    def __init__(self, vocab_file_path):
        super().__init__(vocab_file_path)
        self.trie = Trie(self.vocabulary)
        
        
    def suggest(self, term, distance="levenshtein", threshold=2**31):
    
        assert distance in ["levenshtein", "restricted", "intermediate"]
        
        distanceFunc = None
        if distance == "levenshtein":
            distanceFunc = Distances.levenshtein_trie
        elif distance == "restricted":
            distanceFunc = Distances.damerau_levenshtein_restringida_trie
        else:
            distanceFunc = Distances.damerau_levenshtein_intermedia_trie
        
        words = distanceFunc(self.trie, term, threshold)
        result = {}
        for w,d in words:
            result[self.trie.get_output(w)] = int(d)
        return result
        
    
if __name__ == "__main__":
    spellsuggestertrie = TrieSpellSuggester("./corpora/quijote.txt")
    spellsuggester = SpellSuggester("./data/quijote.txt")
    test = {"casa"}
    for t in test:
        for i in range(1,5):
            result = spellsuggester.suggest("casa", "intermediate", i)
            resultT = spellsuggestertrie.suggest("casa", "intermediate", i)
            print(len(result))
            print(len(resultT))
            print("-------------")
            """ Devuelve uno más ya que incluye la cadena vacia."""
            
                
        
    # cuidado, la salida es enorme print(suggester.trie)

    
