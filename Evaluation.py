import sys


def evaluate(results_file, query_num, relevances):
    with open(results_file) as f:
        lines = f.readlines()
        relevant = 0
        precision = 0
        r_precision = None
        rr = None
        for i, line in enumerate(lines):
            if line.strip().split()[0] in relevances[query_num]:
                if relevant == 0: rr = 1.0/ (i+1)
                relevant += 1
                precision += float(relevant) / (i+1)
            if i+1 == len(relevances[query_num]):
                r_precision = float(relevant) / (i+1)

            
        precision = precision / relevant
        print query_num
        print "AP: ", precision
        print "R-precision: ", r_precision
        print "RR: ", rr
        return precision, r_precision, rr

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

def evaluateEverything():
    relevances = getRelevances()
    mean_precision, mean_r_precision, mrr = 0, 0, 0

    for query_num in range(1, 51):
        if (query_num == 9 or query_num == 49): continue
        precision, r_precision, rr = evaluate("Results/query"+str(query_num)+".txt", query_num, relevances)
        mean_precision += precision
        mean_r_precision += r_precision
        mrr += rr

    mean_precision /= 48
    mean_r_precision /= 48
    mrr /= 48
    print "MAP: ", mean_precision 
    print "Mean R-precision: ", mean_r_precision
    print "MRR: ", mrr


def main():
    evaluateEverything()

if __name__ == "__main__":
    main()

