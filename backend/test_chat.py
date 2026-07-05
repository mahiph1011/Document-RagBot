from services.rag_service import RAGService

rag = RAGService()

print("=" * 70)
print("Enterprise RAG Chatbot")
print("=" * 70)

while True:

    question = input("\nAsk a question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    response = rag.ask(question)

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)

    print(response["answer"])

    print("\n" + "=" * 70)
    print("SOURCES")
    print("=" * 70)

    for source in response["sources"]:

        print(
            f"Document : {source['document']}"
        )

        print(
            f"Section  : {source['section']}"
        )

        print(
            f"Similarity : {source['similarity']}"
        )

        print("-" * 40)