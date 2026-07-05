# testing for pdf 
# from indexing.parsers.pdf_parser import PDFParser

# parser = PDFParser()

# document = parser.parse("data/documents/sample.pdf")

# print(document.summary())

# print()

# print(document.content[:500])





# testing for txt
# from indexing.parsers.txt_parser import TXTParser

# parser = TXTParser()

# doc = parser.parse("data/documents/sample.txt")

# print(doc.summary())





# testing for docx
# from indexing.parsers.docx_parser import DOCXParser

# parser = DOCXParser()

# doc = parser.parse("data/documents/sample.docx")

# print(doc.summary())



# testing for json
# from indexing.parsers.json_parser import JSONParser

# parser = JSONParser()

# document = parser.parse("data/documents/sample.json")

# print("Document Summary")
# print("----------------")
# print(document.summary())

# print("\nExtracted Content")
# print("-----------------")
# print(document.content)



#testing document_service
# from services.document_service import DocumentService

# service = DocumentService()

# print("Supported Formats")

# print(service.supported_extensions())

# print()

# document = service.load_document(
#     "data/documents/sample.pdf"
# )

# print(document.summary())

# print()

# print(document.content[:500])






# testing chunker.py
# from services.document_service import DocumentService
# from indexing.chunker import Chunker

# service = DocumentService()

# document = service.load_document(
#     "data/documents/sample.pdf"
# )

# chunker = Chunker(
#     max_tokens=120,
#     overlap_sentences=1
# )

# chunks = chunker.split(document)

# chunker.preview(chunks)

# print()

# print(chunker.statistics(chunks))



# testing embedding service.py
# from services.document_service import DocumentService
# from indexing.chunker import Chunker
# from services.embedding_service import EmbeddingService

# service = DocumentService()

# document = service.load_document(
#     "data/documents/sample.pdf"
# )

# chunker = Chunker()

# chunks = chunker.split(document)

# embedding_service = EmbeddingService()

# embeddings = embedding_service.embed_documents(chunks)

# print("\n" + "=" * 60)

# print("Embedding Model")
# print(embedding_service.model_name())

# print("\nEmbedding Dimension")
# print(embedding_service.embedding_dimension())

# print("\nNumber of Chunks")
# print(len(chunks))

# print("\nEmbedding Shape")
# print(embeddings.shape)

# print("\nFirst Embedding (First 10 Values)")
# print(embeddings[0][:10])



# vector service testing
# from services.document_service import DocumentService
# from indexing.chunker import Chunker
# from services.embedding_service import EmbeddingService
# from services.vector_service import VectorService

# service = DocumentService()

# document = service.load_document(
#     "data/documents/sample.pdf"
# )

# chunker = Chunker()

# chunks = chunker.split(document)

# embedding_service = EmbeddingService()

# embeddings = embedding_service.embed_documents(
#     chunks
# )

# vector_service = VectorService(
#     embedding_service.embedding_dimension()
# )

# vector_service.add_embeddings(
#     embeddings,
#     chunks
# )

# vector_service.save()

# print()

# print("Chunks Stored")

# print(vector_service.total_documents())

# query = embedding_service.embed_text(
#     "What is the leave policy?"
# )

# results = vector_service.search(
#     query,
#     top_k=3
# )

# print()

# print("Search Results")

# for result in results:

#     print()

#     print(result["score"])

#     print(result["chunk"]["content"][:200])






# # indexer.py testing 
# from indexing.indexer import Indexer

# indexer = Indexer()

# result = indexer.index_document(
#     "data/documents/sample.pdf"
# )

# print()

# print(result)

# print()

# results = indexer.search(
#     "What is the attendance policy?"
# )

# print()

# print("=" * 60)

# print("Retrieved Chunks")

# print("=" * 60)

# for item in results:

#     print()

#     print("Score :", round(item["score"], 4))

#     print()

#     print(item["chunk"]["content"][:250])







"""
test_pdf.py

Debug script for the document parsing and chunking pipeline.
"""

from pprint import pprint

from services.document_service import DocumentService
from indexing.chunker import Chunker

print("=" * 80)
print("Loading document...")
print("=" * 80)

document_service = DocumentService()

document = document_service.load_document(
    "data/documents/sample.pdf"
)

print("\nDocument Loaded Successfully\n")

print("Filename   :", document.filename)
print("Extension  :", document.extension)

# If your Document model has these fields
if hasattr(document, "mime_type"):
    print("MIME Type  :", document.mime_type)

if hasattr(document, "language"):
    print("Language   :", document.language)

if hasattr(document, "word_count"):
    print("Word Count :", document.word_count())

print("\n" + "=" * 80)
print("Chunking Document...")
print("=" * 80)

chunker = Chunker()

chunks = chunker.split(document)

print("\nTotal Chunks :", len(chunks))

print("\n" + "=" * 80)
print("FIRST CHUNK DICTIONARY")
print("=" * 80)

pprint(chunks[0])

print("\n" + "=" * 80)
print("ALL KEYS IN FIRST CHUNK")
print("=" * 80)

print(chunks[0].keys())

print("\n" + "=" * 80)
print("END")
print("=" * 80)