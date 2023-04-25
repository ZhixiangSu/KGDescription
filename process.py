import os
dataset='WN18RR-subset'
# with open(os.path.join(f'save/{dataset}/', "entity2textOpenAI.txt"), 'r', encoding='utf-8') as f1,\
#     open(os.path.join(f'save/{dataset}/', "entity2textOpenAI2.txt"), 'w', encoding='utf-8') as f2:
#     for line in f1:
#         line=line.split("\t")
#         new_line=line[0]+"\t"+" ".join(line[1:])
#         f2.write(new_line)

with open(os.path.join(f'save/{dataset}/', "entity2textWikipedia.txt"), 'r', encoding='utf-8') as f1, \
    open(os.path.join(f'data/{dataset}/', "entity2text.txt"), 'r', encoding='utf-8') as f2:
    i=0
    for line1,line2 in zip(f1,f2):
        i+=1
        e1 = line1.split("\t")[0]
        e2 = line2.split("\t")[0]
        if e1!=e2:
            print(e1)
            print(e2)
            print()