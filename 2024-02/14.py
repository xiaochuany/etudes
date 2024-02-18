
def get_stats(s:str):
    count = {}
    for c1,c2 in zip(s,s[1:]):
        count[(c1,c2)] = count.get((c1,c2),0)+1
    return count

def encode(ids, merges):
    i = 0
    t = None
    new_ids = []
    while i<len(ids[:-1]):
        if not t: 
            if (ids[i],ids[i+1]) not in merges:
                new_ids.append(ids[i])
            else: 
                t = merges[(ids[i],ids[i+1])]
        else:
            if (t,ids[i+1]) not in merges:
                new_ids.append(t)
                t = None
            else:
                t = merges[(t,ids[i+1])]
        i+=1
    return new_ids

print(get_stats('abbabc'))

print(encode([1,2,1,5,1,8,8,1,5], {(1,5):8, (8,1):9}))
