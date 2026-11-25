# Catalog Assistant (presales)

Streamlit chat app that answers presales questions about two fictional companies
(CircuitNova, Hearthwell) from 5 Excel sheets per company and 5 policy documents.

- Main file for hosting: `catalog-agentic-rag-reference/app.py`
- Secrets (set in the host, never in git): `GROQ_API_KEY`, `NVIDIA_API_KEY`
- Rebuild the database from the Excel files: `python catalog-agentic-rag-reference/load_data.py`
