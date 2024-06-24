import chromadb
from chromadb.utils import embedding_functions
from review_data_etl import prepare_reviews_data
from chroma_utils import build_chroma_collection


DATA_PATH = "data/*"
CHROMA_PATH = "review_embeddings"
EMBEDDING_FUNC_NAME = "multi-qa-MiniLM-L6-cos-v1" # model specifically trained to solve question-and-answer semantic search tasks
COLLECTION_NAME = "app_reviews"

chroma_reviews_dict = prepare_reviews_data(DATA_PATH)

build_chroma_collection(
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBEDDING_FUNC_NAME,
    chroma_reviews_dict["ids"],
    chroma_reviews_dict["documents"],
    chroma_reviews_dict["metadatas"]
)


client = chromadb.PersistentClient(CHROMA_PATH)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_FUNC_NAME)
collection = client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_func)

great_reviews = collection.query(query_texts=["Find me some positive reviews that discuss the car's performance"],
                                 n_results=5,
                                 include=["documents", "distances", "metadatas"])

great_reviews["documents"][0][0]
' Great all around car with great balance of performance and comfort. Terrific technology too.'