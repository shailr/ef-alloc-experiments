import os
from sys import maxsize
import numpy as np
from utils.filerw import readdat

additive_utililty = lambda alloc, utility : sum(np.array(alloc) * np.array(utility))

def complementing_utility(alloc, utility, p_utility) :
    pairwise_alloc = []
    for i in range(0, len(alloc), 2):
        pairwise_alloc.append(alloc[i] & alloc[i+1])
    return additive_utililty(alloc, utility) + additive_utililty(pairwise_alloc, p_utility)

def envyMap(allocs, utilities, p_utilities):
    size_agents = np.array(allocs).shape[0]
    envy_map = np.zeros((size_agents, size_agents))
    for i in range(len(envy_map)):
        for j in range(len(envy_map[i])):
            envy_map[i][j] = complementing_utility(allocs[i], utilities[i], p_utilities[i]) \
            - complementing_utility(allocs[j], utilities[i], p_utilities[i])
    return envy_map

def envyMap_upto1(allocs, utilities, p_utilities):
    size_agents = np.array(allocs).shape[0]
    size_res = np.array(allocs).shape[1]
    envy_map = np.zeros((size_agents, size_agents))
    for i in range(len(envy_map)) :
        for j in range(len(envy_map[i])):
            envy_map[i][j] = complementing_utility(allocs[i], utilities[i], p_utilities[i]) \
            - complementing_utility(allocs[j], utilities[i], p_utilities[i])
            if envy_map[i][j] < 0 :
                envy_res_drop1_j = np.zeros(size_res)
                max_pos_envy = - maxsize
                for x in range(len(envy_res_drop1_j)) :
                    new_alloc_j = list(allocs[j])
                    new_alloc_j[x] = 0
                    envy_res_drop1_j[x] = complementing_utility(allocs[i], utilities[i], p_utilities[i]) \
                    - complementing_utility(new_alloc_j, utilities[i], p_utilities[i])
                    # print(envy_res_drop1_j)
                    if envy_res_drop1_j[x] >= max_pos_envy:
                        envy_map[i][j] = envy_res_drop1_j[x]
                        max_pos_envy = envy_res_drop1_j[x]
                
    return envy_map

def envyMap_upto2(allocs, utilities, p_utilities):
    size_agents = np.array(allocs).shape[0]
    size_res = np.array(allocs).shape[1]
    envy_map = np.zeros((size_agents, size_agents))
    for i in range(len(envy_map)) :
        for j in range(len(envy_map[i])):
            envy_map[i][j] = complementing_utility(allocs[i], utilities[i], p_utilities[i]) \
            - complementing_utility(allocs[j], utilities[i], p_utilities[i])
            if envy_map[i][j] < 0 :
                envy_res_drop1_j = np.zeros(size_res)
                max_pos_envy = - maxsize
                for x in range(len(envy_res_drop1_j)) :
                    new_alloc_j = list(allocs[j])
                    new_alloc_j[x] = 0
                    envy_res_drop1_j[x] = complementing_utility(allocs[i], utilities[i], p_utilities[i]) \
                    - complementing_utility(new_alloc_j, utilities[i], p_utilities[i])
                    # print(envy_res_drop1_j)
                    if envy_res_drop1_j[x] >= max_pos_envy:
                        envy_map[i][j] = envy_res_drop1_j[x]
                        max_pos_envy = envy_res_drop1_j[x]
                        if envy_map[i][j] < 0 :
                            envy_res_drop2_j = np.zeros((size_res, size_res))
                            max_pos_envy_drop2 = - maxsize
                            for p in range(len(envy_res_drop2_j)):
                                for q in range(len(envy_res_drop2_j[p])):
                                    if p == q:
                                        continue
                                    new_alloc_j_drop2 = list(allocs[j])
                                    new_alloc_j_drop2[p] = 0
                                    new_alloc_j_drop2[q] = 0
                                    envy_res_drop2_j[p][q] = complementing_utility(allocs[i], utilities[i], p_utilities[i]) \
                                    - complementing_utility(new_alloc_j_drop2, utilities[i], p_utilities[i])
                                    if envy_res_drop2_j[p][q] >= max_pos_envy_drop2:
                                        envy_map[i][j] = envy_res_drop2_j[p][q]
                                        max_pos_envy_drop2 = envy_res_drop2_j[p][q]
                
    return envy_map

def ef_percent(dir_name):
    Us, Vs, As = readdat(dir_name)
    Us = np.array(Us)
    Vs = np.array(Vs)
    As = np.array(As)
    print("Us shape :", Us.shape)
    print("Vs shape :", Vs.shape)
    print("As shape :", As.shape)
    
    ef_map = []
    envymap0 = []
    for i in range(1000):
        envymaptemp = envyMap(As[i], Us[i], Vs[i])
        envymap0.append(envymaptemp)
        # print(envymaptemp)
        ef_map.append(not bool(np.sum(envymaptemp<0)))

    ef_map = np.array(ef_map)
    envymap0 = np.array(envymap0)
    # print(ef_map)
    print("EF0 percent : ", np.sum(ef_map)/len(ef_map) * 100)

    ef1_map = []
    envymap1 = []
    for i in range(1000):
        envymaptemp = envyMap_upto1(As[i], Us[i], Vs[i])
        envymap1.append(envymaptemp)
        # print(envymaptemp)
        ef1_map.append(not bool(np.sum(envymaptemp<0)))

    ef1_map = np.array(ef1_map)
    envymap1 = np.array(envymap1)
    # print(ef_map)
    print("EF1 percent : ", np.sum(ef1_map)/len(ef1_map) * 100)

    ef2_map = []
    envymap2 = []
    for i in range(1000):
        envymaptemp = envyMap_upto2(As[i], Us[i], Vs[i])
        envymap2.append(envymaptemp)
        # print(envymaptemp)
        ef2_map.append(not bool(np.sum(envymaptemp<0)))

    ef2_map = np.array(ef2_map)
    envymap2 = np.array(envymap2)
    # print(ef_map)
    print("EF2 percent : ", np.sum(ef2_map)/len(ef2_map) * 100)
    
    print("Means: envy")
    print(np.mean(envymap0, axis=0))
    print(np.mean(envymap1, axis=0))
    print(np.mean(envymap2, axis=0))
    
    print("Means: max(0, envy)")
    print(np.mean(envymap0.clip(min=0), axis=0))
    print(np.mean(envymap1.clip(min=0), axis=0))
    print(np.mean(envymap2.clip(min=0), axis=0))
        
    print("Means: min(0, envy)")
    print(np.mean(envymap0.clip(max=0), axis=0))
    print(np.mean(envymap1.clip(max=0), axis=0))
    print(np.mean(envymap2.clip(max=0), axis=0))
    
    print("Stds")
    print(np.std(envymap0, axis=0))
    print(np.std(envymap1, axis=0))
    print(np.std(envymap2, axis=0))
    
    return (envymap0, envymap1, envymap2)
