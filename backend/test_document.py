from models.document_model import Document

doc = Document(
    filename="sample.pdf",
    extension=".pdf",
    content="Hello this is my first document.",
    source_path="data/documents/sample.pdf"
)

print(doc.summary())