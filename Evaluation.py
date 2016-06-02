import sys


def evaluate(results_file, query_num, relevances):
    with open(results_file) as f:
        lines = f.readlines()
        relevant = 0
        precision = 0
        r_precision = None
        for i, line in enumerate(lines):
            if line.strip().split()[0] in relevances[query_num]:
                relevant += 1
                precision += float(relevant) / (i+1)
            if i+1 == len(relevances[query_num]):
                r_precision = float(relevant) / (i+1)

            
        precision = precision / relevant
        print query_num
        print "AP: ", precision
        print "R-precision", r_precision
        return precision, r_precision

def getRelevances():
    relevances = {}
    with open("relevance-judgements.txt") as f:
        for line in f:
            line = line.strip().split()
            if len(line) > 1:
                query = int(line[0][5:])
                article = line[1]
                if query in relevances:
                    relevances[query].append(article)
                else:
                    relevances[query] = [article]
    return relevances


def main():
    relevances = getRelevances()
    mean_precision, mean_r_precision = 0, 0 

    for query_num in range(1, 51):
        precision, r_precision = evaluate("Results/query"+str(query_num)+".txt", query_num, relevances)
        mean_precision += precision
        mean_r_precision += r_precision

    mean_precision /= 48
    mean_r_precision /= 48
    print "MAP: ", mean_precision 
    print "Mean R-precision", mean_r_precision
    

if __name__ == "__main__":
    main()

