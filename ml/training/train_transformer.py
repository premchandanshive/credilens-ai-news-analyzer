"""
CrediLens — Transformer Fine-Tuning Pipeline (DistilBERT)
Provides fine-tuning template for sequence classification with Hugging Face Transformers.
"""

import os
import csv

def train_transformer(
    model_name='distilbert-base-uncased',
    dataset_path='ml/datasets/sample_news.csv',
    output_dir='ml/saved_models/distilbert_credilens',
    epochs=3,
    batch_size=8,
    lr=2e-5
):
    print(f"Preparing transformer training pipeline with base model {model_name}...")
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch
    except ImportError:
        print("Transformers or PyTorch package not installed. Skipping transformer training.")
        return

    texts = []
    labels = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            combined = (row.get('title') or '') + ' ' + (row.get('text') or '')
            texts.append(combined)
            labels.append(1 if row.get('label') == 'reliable' else 0)

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        os.makedirs(output_dir, exist_ok=True)
        tokenizer.save_pretrained(output_dir)
        print(f"Transformer tokenizer initialized and saved to {output_dir}")
    except Exception as e:
        print(f"Note: Transformer download skipped or offline: {e}")

if __name__ == '__main__':
    train_transformer()
