"""
Purpose: Multi-format document loaders extracting text from PDF, DOCX, TXT, and Markdown files.
Inputs: File path or binary file stream of uploaded document.
Outputs: List of extracted Document objects with page content and metadata.
Dependencies: pypdf, python-docx, app.core.config.
TODOs:
  - Implement PDF loader utilizing pypdf to extract page-by-page text.
  - Implement DOCX loader extracting paragraphs and tables using python-docx.
  - Implement plain text and Markdown file loaders.
"""
