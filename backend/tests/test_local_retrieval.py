from backend.src.services.retrieval.local_retrieval import (
    LocalRetrievalService
)

retrieval = LocalRetrievalService()

results = retrieval.retrieve_rules(
    query="sponsored content disclosure requirements",
    k=3
)

print("\nRESULTS:\n")

for i, doc in enumerate(results, start=1):
    print(f"\n--- Document {i} ---\n")
    print(doc[:500])