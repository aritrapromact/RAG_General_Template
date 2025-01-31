from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="Alibaba-NLP/gte-large-en-v1.5",
                                   model_kwargs = {'trust_remote_code': True})

if __name__ == '__main__':
    print("Hello World")
    sentences = "That is a happy person"
    embeddings = embeddings.embed_query(sentences)
    # print(similarities.shape)
    print(len(embeddings))
    # [4, 4]

