import numpy as np

additive_utililty = lambda alloc, utility : sum(np.array(alloc) * np.array(utility))

def complementing_utility(alloc, utility, p_utility) :
    pairwise_alloc = []
    for i in range(0, len(alloc), 2):
        pairwise_alloc.append(alloc[i] & alloc[i+1])
    return additive_utililty(alloc, utility) + additive_utililty(pairwise_alloc, p_utility)

def optimal_nash_prod_wcomp(utility, p_utility) :
    n = len(utility)
    if n :
        m = len(utility[0])
        
    optimal_alloc = np.zeros((n, m))
    opt_payoff = 0
    for i in range(2**(m*n)) :
        curr_alloc = np.array([int(x) for x in list(np.binary_repr(i, width=(m*n)))]).reshape(n, m).tolist()
        req_resources = np.zeros(m)
        payoff = 1
        # print(curr_alloc)
        for j in range(len(curr_alloc)) :
            req_resources += curr_alloc[j]
        if not np.array_equal(req_resources, np.ones(m)) :
            continue
        for j in range(len(curr_alloc)) :
            payoff *= complementing_utility(curr_alloc[j], utility[j], p_utility[j])
            
        if opt_payoff < payoff :
            opt_payoff = payoff
            optimal_alloc = curr_alloc
            
    return(optimal_alloc)

def writeNashAlloc(U, V, na, seed):
    filename = "nash_allocs_random_uv_" + str(seed)
    file = open(filename, "a")
    file.write("%s %s \t # U Shape\n" %(len(U), len(U[0])))
    for i in range(len(U)):
        file.write(" ".join(str(x) for x in U[i]))
        file.write("\n")
    
    file.write("%s %s \t # V Shape\n"  %(len(V), len(V[0])))
    for i in range(len(V)):
        file.write(" ".join(str(x) for x in V[i]))
        file.write("\n")
    
    file.write("%s %s \t # Alloc Shape\n"  %(len(na), len(na[0])))
    for i in range(len(na)):
        file.write(" ".join(str(x) for x in na[i]))
        file.write("\n")
        
    file.write("\n")
    file.close()

for s in range(10, 20):
    np.random.seed(s)
    
    for x in range(100):
        m = 10
        R = [(i, np.random.randint(0, 100)) for i in range(m)]

        n = 2
        N = [(i, np.random.randint(0, 100), np.random.randint(0, 100)) for i in range(n)]

        U = []
        for index, i in enumerate(N):
            u_i = np.random.random_sample(len(R)) * 100
            U.append(u_i)

        V = []
        for index, i in enumerate(N):
            v_ijjp1 = np.random.random_sample(len(R)//2) * 100
            V.append(v_ijjp1)

        nashp_alloc = optimal_nash_prod_wcomp(U, V)

        writeNashAlloc(U, V, nashp_alloc, s)
