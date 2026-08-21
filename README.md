# Hotel AI - Intelligent Hotel Assistant

## Project Overview
Hotel AI is an intelligent hotel assistant project designed to support
hotel-related question answering, structured FAQ data, knowledge retrieval,
and RAG-based responses.

## Main Components

- `02_Hotel_Knowledge/`
  - Hotel knowledge base and policy documents.

- `03_Structured_Data/`
  - FAQ datasets, intents, JSON configuration, batches, reports, and backups.

- `data/`
  - Synthetic hotel operational data.

- `database/`
  - Database backup.

- `scripts/`
  - Data generation and validation notebooks.

## Master FAQ Dataset

The production FAQ dataset is:

`03_Structured_Data/CSV/final/hotel_faq_final.csv`

Current master size:
- 448 FAQs
- 8 intents
- 4 languages

## RAG Knowledge Base

The main knowledge sources are stored under:

`02_Hotel_Knowledge/`

## Data Quality

All production data should pass:
- structural validation
- duplicate validation
- semantic validation
- factual validation
- language validation
- RAG grounding validation
