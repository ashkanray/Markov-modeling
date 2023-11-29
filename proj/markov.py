from hashtable import Hashtable
import math
import time

HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    def __init__(self, k, text, use_hashtable):
        """Construct a new k-order markov model using the text 'text'."""
        self.k = k
        self.text = text
        self.unqiues = self.__find_uniques()
        self.use_hash = use_hashtable
        
        if use_hashtable:
            #####TIMER
            start = time.perf_counter()
            self.markov = Hashtable(HASH_CELLS, 0, TOO_FULL, GROWTH_RATIO)
            self.create_model()
            elapsed = time.perf_counter() - start
        else:
            self.markov = {}
            self.create_model()


    def create_model(self):
        iterate_text = self.text + self.text[:self.k]

        for i in range(len(self.text)):
            k = iterate_text[i:i+self.k]
            k_1 = iterate_text[i:i+self.k+1]
            

            if k not in self.markov:
                self.markov[k] = 1
            else:
                self.markov[k] = self.markov[k] + 1
            
            if k_1 not in self.markov:
                self.markov[k_1] = 1
            else:
                self.markov[k_1] = self.markov[k_1] + 1
            


    def __find_uniques(self):
        uniq_list = []
        for char in self.text:
            if char not in uniq_list:
                uniq_list.append(char)

        return uniq_list      



    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """
        iterate_text = s + s[:self.k]
        total_log = 0
        S = len(self.unqiues)

        for i in range(len(s)):
            k = iterate_text[i:i+self.k]
            k_1 = iterate_text[i:i+self.k+1]

            try: 
                M = self.markov[k_1]
            except:
                M = 0
            
            try:
                N = self.markov[k]
            except:
                N = 0

            total_log += math.log((M+1)/(N+S))
        
        return total_log



def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """


    model_1 = Markov(k, speech1, use_hashtable)
    model_1_log = model_1.log_probability(speech3) / len(speech3)

    model_2 = Markov(k, speech2, use_hashtable)
    model_2_log = model_2.log_probability(speech3) / len(speech3)


    if model_1_log > model_2_log:
        return (model_1_log, model_2_log, "A")
    else: 
        return (model_1_log, model_2_log, "B")



if __name__ == "__main__":
    filenameA = "./speeches/bush1+2.txt"
    filenameB = "./speeches/kerry1+2.txt"
    filenameC = "./speeches/bush-kerry3/BUSH-0.txt"

    try:
        with open (filenameA, 'r') as fileA:
            speech1 = fileA.read()

        with open (filenameB, 'r') as fileB:
            speech2 = fileB.read()

        with open (filenameC, 'r') as fileC:
            speech3 = fileC.read()
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

    k = 2
    use_hashtable = True
    ####TIMER
    start = time.perf_counter()
    print(identify_speaker(speech1, speech2, speech3, k, use_hashtable))
    elapsed = time.perf_counter() - start

    print("Total time: %f seconds for k = %d" %(elapsed, k))
    
