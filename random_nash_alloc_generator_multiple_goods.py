import numpy as np
import random

additive_utililty = lambda alloc, utility : sum(np.array(alloc) * np.array(utility))

def complementing_utility(alloc, utility, p_utility) :
    pairwise_alloc = []
    for i in range(0, len(alloc), 2):
        if alloc[i] == 0 or alloc[i+1] == 0:
            pairwise_alloc.append(0)
        else:
            pairwise_alloc.append(alloc[i] if alloc[i] < alloc[i+1] else alloc[i+1])
    return additive_utililty(alloc, utility) + additive_utililty(pairwise_alloc, p_utility)

def optimal_nash_prod_multires(utility_f, agents, resources, utility, p_utility):
    num_a = len(agents)
    num_r = len(resources)
    total_res = np.array(resources)[:,1]
    avail_res = total_res

    allocs = np.zeros((num_a, num_r))
    flallocs = allocs.flatten()
    
    opt_allocs = allocs
    opt_payoff = 0
    
    counter = 0
    while not np.array_equal(allocs[-1], total_res):
        i = 0
        carry = True
        while i < len(flallocs) and carry:
            carry = False
            flallocs[i] += 1
            if avail_res[i%len(avail_res)] == 0:
                carry = True
                flallocs[i] = 0
            i += 1
            allocs = flallocs.reshape((num_a, num_r))
            avail_res = total_res - allocs.sum(axis=0)
        payoff = 1
        for j in range(len(allocs)) :
            payoff *= utility_f(allocs[j], utility[j], p_utility[j])
        if opt_payoff < payoff :
            opt_payoff = payoff
            opt_allocs = np.copy(allocs)
        counter += 1
    return opt_allocs

def writeNashAlloc(N, R, U, V, na, seed):
    filename = "nash_allocs_random_uv_" + str(seed)
    file = open(filename, "a")
    
    file.write("%s %s \t # N Shape\n" %(len(N), len(N[0])))
    for i in range(len(N)):
        file.write(" ".join(str(x) for x in N[i]))
        file.write("\n")

    file.write("%s %s \t # R Shape\n" %(len(R), len(R[0])))
    for i in range(len(R)):
        file.write(" ".join(str(x) for x in R[i]))
        file.write("\n")

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
        m = 2
        q = 3
        # id, quantity_available, cost
        R = [(i, np.random.randint(1, q+1), np.random.randint(0, 100)) for i in range(m)]
        RQ = np.array(R)[:,1]
        
        n = 2
        # id, quantity_owned, capacity, priority
        N = [(i, 0, np.random.randint(0, 100), np.random.randint(0, 100)) for i in range(n)]
        
        U = []
        for index, i in enumerate(N):
            u_i = random.sample(range(0, 100), len(R))
            U.append(u_i)

        V = []
        for index, i in enumerate(N):
            # No complementing utility
            v_ijjp1 = np.random.random_sample(len(R)//2) * 0

            # Complementing utility
            # v_ijjp1 = np.random.random_sample(len(R)//2) * 100

            # Substitutive utility 1
#             v_ijjp1 = []
#             for j in range(0, len(U[index]), 2):
#                 v_ijjp1.append(max(U[index][j], U[index][j+1]))
#             v_ijjp1 = np.array(v_ijjp1)

            # Substitutive utility 2
#             v_ijjp1 = []
#             for j in range(0, len(U[index]), 2):
#                 v_ijjp1.append(U[index][j] + U[index][j+1] - np.random.uniform(0, min(U[index][j], U[index][j+1]), 1)[0])
#             v_ijjp1 = np.array(v_ijjp1)

            V.append(v_ijjp1)

        nashp_alloc = optimal_nash_prod_multires(complementing_utility, N, R, U, V)

        writeNashAlloc(N, R, U, V, nashp_alloc, s)
