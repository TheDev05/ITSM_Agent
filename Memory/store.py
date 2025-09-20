from langgraph.store.memory import InMemoryStore
from Models.embedding import embeddings

store = InMemoryStore(
    index = {
        'embed' : embeddings,
        'dims' : 1536
    }
)