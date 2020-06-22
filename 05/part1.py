from collections import defaultdict
from operator import itemgetter

if __name__ == "__main__":
    
    with open('05/input') as f:
        p = [ord(i) for i in f.readline().strip()]
        #p = [ord(i) for i in 'dabAcCaCBAcCcaDA']

        print(len(p))
        start = len(p)-1 
        while True:
            if start >= len(p):
                start = len(p) - 1
            reduced = True
            for pos in range(start, 0, -1):
                if p[pos] ^ p[pos-1] == 32:
                    del p[pos-1:pos+1]
                    reduced = False
                    start = pos                
                    break
            if reduced:
                break
        print(len(p))
# PART 2
    with open('05/input') as f:
        polymer = [ord(i) for i in f.readline().strip()]
        #polymer = [ord(i) for i in 'dabAcCaCBAcCcaDA']

        types = set(i | 32 for i in polymer)
        results = defaultdict(int)

        for p_type in types:
            p = polymer[:]
            for pos in range(len(p)-1, -1, -1):
                if p[pos] | 32 == p_type:
                        del p[pos]
                                                
            start = len(p)-1 
            while True:
                reduced = True
                if start >= len(p):
                    start = len(p) - 1
                for pos in range(start, 0, -1):                    
                    if p[pos] ^ p[pos-1] == 32:
                        del p[pos-1:pos+1]
                        reduced = False
                        start = pos                     
                        break
                if reduced:
                    break
            results[p_type] = len(p)
            #print(chr(p_type), len(p), [chr(i) for i in p])
        a, b = min(results.items(), key=itemgetter(1))
        print(chr(a), b)