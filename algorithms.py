import math
import textdistance

#D is the input dataset
def algorithm1(D):
    size_indexes = []
    sorted_words = []
    a = len(max(D,key=len))
    #the range must be a+2, because we must insert the index with len equal to "a"
    #thus we also need the index of the "a+1" position for future usage (Algorithm2)
    multi_vector = [[] for i in range(a+2)]
    for i in range(len(D)):
        multi_vector[len(D[i])].append(D[i])
    for i in range(a+2):
        size_indexes.append(len(sorted_words))
        for j in range(len(multi_vector[i])):
            sorted_words.append(multi_vector[i][j])
    return size_indexes,sorted_words, a

#D is the inpute dataset, threshold is the lower bound threhsold for similarity functions
#sim is the desired similarity function, and beta is the factor that influences in the length filter
#the patterns functions formulas employ beta = 1
#q is the Q value employed by the filters associated with the executions
def algorithm2(D,threshold,sim, beta, extra_filter,q):
    size_indexes,sorted_words,a = algorithm1(D)
    similar_pairs = []
    #simfunc = {1:"Cosine",2:"Dice",3:"Jaccard",4:"Jaro",5:"Normalized Levenshtein"}
    ftau = [1/(thresahold**2),(2-threshold)/threshold,1/threshold,1/abs((3*threshold)-2),1/threshold]
    #filters = {0:"Exeution only with the length filter", 1:"Strings shares the q first characters", 2:"Strings has more than 50% of similarity in the first q-gram"}
    lf = abs(1-ftau[sim-1])
    match sim:
        case 1:
            return Cosine(size_indexes,sorted_words,a,threshold,lf,beta,extra_filter,q)
        case 2:
            return Dice(size_indexes,sorted_words,a,threshold,lf,beta,extra_filter,q)
        case 3:
            return Jaccard(size_indexes,sorted_words,a,threshold,lf,beta,extra_filter,q)
        case 4:
            return Jaro(size_indexes,sorted_words,a,threshold,lf,beta,extra_filter,q)
        case 5:
            return Levenshtein(size_indexes,sorted_words,a,threshold,lf,beta,extra_filter,q)

#Cosine similarity function
def Cosine(size_indexes,sorted_words,a,threshold,lf,beta,extra_filter,q):   
    if(extra_filter == 0):
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                similarity = textdistance.cosine(sorted_words[i],sorted_words[j])
                if(similarity>=threshold):
                    similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs
    if(extra_filter == 1):
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                if(sorted_words[j].startswith(sorted_words[i][0:q])):
                    similarity = textdistance.cosine(sorted_words[i],sorted_words[j])
                    if(similarity>=threshold):
                        similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs
    else:
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                if(textdistance.cosine(sorted_words[j][0:q],sorted_words[i][0:q])>0.5):
                    similarity = textdistance.cosine(sorted_words[i],sorted_words[j])
                    if(similarity>=threshold):
                        similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs

#Sorensen-Dice Coeficcient                                   
def Dice(size_indexes,sorted_words,a,threshold,lf,beta,extra_filter,q):
    if(extra_filter == 0):
        similar_pairs = []
        for i in range(len(sorted_words)):
            Na = len(sorted_words[i])
            limit = math.floor(Na+(Na*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                similarity = textdistance.sorensen(sorted_words[i],sorted_words[j])
                if(similarity>=threshold):
                    similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs
    if(extra_filter == 1):
        similar_pairs = []
        for i in range(len(sorted_words)):
            Na = len(sorted_words[i])-(q-1)
            limit = math.floor(Na+(Na*lf*beta))+(q-1)
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                if(sorted_words[j].startswith(sorted_words[i][0:q])):
                    similarity = textdistance.sorensen(sorted_words[i],sorted_words[j])
                    if(similarity>=threshold):
                        similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs
    else:
        similar_pairs = []
        for i in range(len(sorted_words)):
            Na = len(sorted_words[i])-(q-1)
            limit = math.floor(Na+(Na*lf*beta))+(q-1)
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                if(textdistance.cosine(sorted_words[j][0:q],sorted_words[i][0:q])>0.5):
                    similarity = textdistance.sorensen(sorted_words[i],sorted_words[j])
                    if(similarity>=threshold):
                        similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs

#Jaccard similarity function 
def Jaccard(size_indexes,sorted_words,a,threshold,lf,beta,extra_filter,q):
    if(extra_filter == 0):
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                similarity = textdistance.jaccard(sorted_words[i],sorted_words[j])
                if(similarity>=threshold):
                    similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs
    
    if(extra_filter == 1):
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                if(sorted_words[j].startswith(sorted_words[i][0:q])):
                    similarity = textdistance.jaccard(sorted_words[i],sorted_words[j])
                    if(similarity>=threshold):
                        similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs
    else:
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                if(textdistance.cosine(sorted_words[j][0:q],sorted_words[i][0:q])>0.5):
                    similarity = textdistance.jaccard(sorted_words[i],sorted_words[j])
                    if(similarity>=threshold):
                        similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs

#Jaro similarity function
def Jaro(size_indexes,sorted_words,a,threshold,lf,beta,extra_filter,q):
    if(extra_filter == 0):
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+abs(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                similarity = textdistance.jaro(sorted_words[i],sorted_words[j])
                if(similarity>=threshold):
                    similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs
    if(extra_filter == 1):
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+abs(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                if(sorted_words[j].startswith(sorted_words[i][0:q])):
                    similarity = textdistance.jaro(sorted_words[i],sorted_words[j])
                    if(similarity>=threshold):
                        similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs
    else:
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                if(textdistance.cosine(sorted_words[j][0:q],sorted_words[i][0:q])>0.5):
                    similarity = textdistance.jaro(sorted_words[i],sorted_words[j])
                    if(similarity>=threshold):
                        similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs

#Normalized Levenshtein Distance
def Levenshtein(size_indexes,sorted_words,a,threshold,lf,beta,extra_filter,q):
    if(extra_filter == 0):
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+abs(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                similarity = textdistance.levenshtein(sorted_words[i],sorted_words[j])
                normalized_similarity = (len(sorted_words[j]) - similarity)/(len(sorted_words[j]))
                if(normalized_similarity>=threshold):
                    similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs
    if(extra_filter == 1):
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+abs(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                if(sorted_words[j].startswith(sorted_words[i][0:q])):
                    similarity = textdistance.levenshtein(sorted_words[i],sorted_words[j])
                    normalized_similarity = (len(sorted_words[j]) - similarity)/(len(sorted_words[j]))
                    if(normalized_similarity>=threshold):
                        similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs
    else:
        similar_pairs = []
        for i in range(len(sorted_words)):
            limit = math.floor(len(sorted_words[i])+abs(len(sorted_words[i])*lf*beta))
            if(limit>a):
                limit = a
            for j in range(i+1,size_indexes[limit+1]):
                if(textdistance.cosine(sorted_words[j][0:q],sorted_words[i][0:q])>0.5):
                    similarity = textdistance.levenshtein(sorted_words[i],sorted_words[j])
                    normalized_similarity = (len(sorted_words[j]) - similarity)/(len(sorted_words[j]))
                    if(normalized_similarity>=threshold):
                        similar_pairs.append((sorted_words[i],sorted_words[j]))
        return similar_pairs
