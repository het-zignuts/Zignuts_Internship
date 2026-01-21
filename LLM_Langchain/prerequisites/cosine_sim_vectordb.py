import numpy as np 

np.random.seed(42)

embed1=np.random.randn(4)

embed2=np.random.randn(4)

def calculate_cosine_sim(A, B):
    A_mag=np.sqrt(sum(a**2 for a in A))
    B_mag=np.sqrt(sum(b**2 for b in B))
    A_dot_B=sum(a*b for a,b in zip(A,B))
    cosine_similarity=A_dot_B/(A_mag*B_mag)
    return cosine_similarity

print(f"Cosine similarity of embeddings {embed1} and {embed2} is {calculate_cosine_sim(embed1, embed2)}.\n")

embed_dict={
    "emb1": np.random.randn(4),
    "emb2": np.random.randn(4),
    "emb3": np.random.randn(4),
    "emb4": np.random.randn(4)
}

query_embed=np.random.randn(4)

similar_embeds=[]

for k, v in embed_dict.items():
    cs_score=calculate_cosine_sim(v, query_embed)
    similar_embeds.append((v, cs_score))

similar_embeds.sort(key=lambda tup: tup[1], reverse=True)

for elem in similar_embeds:
    print("Embedding : ", elem[0], " Similarity: ", elem[1])
