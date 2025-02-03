from langchain_huggingface import HuggingFaceEmbeddings

embed_model = HuggingFaceEmbeddings(model_name="Alibaba-NLP/gte-base-en-v1.5",
                                   model_kwargs = {'trust_remote_code': True})
EMBEDDING_MODEL_VECTOR_LENGTH = len(embed_model.embed_query("Hello World"))


if __name__ == '__main__':
    print("Hello World")
    sentences = "That is a happy person"
    embeddings = embeddings.embed_query(sentences)
    # print(similarities.shape)
    print(len(embeddings))
    # [4, 4]

