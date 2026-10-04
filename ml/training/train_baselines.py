"""
CrediLens — Baseline Machine Learning Classifiers
Trains TF-IDF + Logistic Regression, TF-IDF + Linear SVM, and Multinomial Naive Bayes.
Saves the production model pipeline artifact to ml/saved_models/tfidf_logreg_credilens.joblib
and generates evaluation metrics in ml/evaluation/METRICS.md.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_predict

def load_data(filepath='ml/datasets/sample_news.csv'):
    df = pd.read_csv(filepath)
    df['combined_text'] = df['title'].fillna('') + ' ' + df['text'].fillna('')
    df['target'] = (df['label'] == 'reliable').astype(int)
    return df

def train_and_evaluate():
    df = load_data()
    X = df['combined_text']
    y = df['target']
    
    models = {
        'TF-IDF + Logistic Regression': Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=5000, sublinear_tf=True)),
            ('clf', LogisticRegression(C=1.0, max_iter=1000, random_state=42))
        ]),
        'TF-IDF + Linear SVM': Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=5000, sublinear_tf=True)),
            ('clf', CalibratedClassifierCV(LinearSVC(C=1.0, random_state=42), cv=3))
        ]),
        'TF-IDF + Multinomial Naive Bayes': Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
            ('clf', MultinomialNB(alpha=1.0))
        ])
    }
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    results = {}
    
    for name, pipeline in models.items():
        y_pred = cross_val_predict(pipeline, X, y, cv=cv)
        acc = accuracy_score(y, y_pred)
        prec = precision_score(y, y_pred, zero_division=0)
        rec = recall_score(y, y_pred, zero_division=0)
        f1 = f1_score(y, y_pred, zero_division=0)
        cm = confusion_matrix(y, y_pred)
        
        results[name] = {
            'accuracy': float(acc),
            'precision': float(prec),
            'recall': float(rec),
            'f1': float(f1),
            'confusion_matrix': cm
        }
        print(f"{name} -> Acc: {acc:.4f}, Prec: {prec:.4f}, Rec: {rec:.4f}, F1: {f1:.4f}")
    
    # Fit the production model on full dataset
    prod_pipeline = models['TF-IDF + Logistic Regression']
    prod_pipeline.fit(X, y)
    
    # Save the artifact
    os.makedirs('ml/saved_models', exist_ok=True)
    artifact_path = 'ml/saved_models/tfidf_logreg_credilens.joblib'
    joblib.dump(prod_pipeline, artifact_path)
    print(f"Saved production model artifact to {artifact_path}")
    
    # Write METRICS.md
    os.makedirs('ml/evaluation', exist_ok=True)
    with open('ml/evaluation/METRICS.md', 'w', encoding='utf-8') as f:
        f.write('# CrediLens ML Model Evaluation Metrics\n\n')
        f.write('This document details the cross-validated performance of baseline text classification models for credibility prediction.\n\n')
        f.write('## Model Comparison (5-Fold Stratified Cross-Validation)\n\n')
        f.write('| Model | Accuracy | Precision (Reliable) | Recall (Reliable) | F1-Score |\n')
        f.write('|---|---|---|---|---|\n')
        for name, m in results.items():
            f.write(f"| **{name}** | {m['accuracy']:.4f} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1']:.4f} |\n")
        
        f.write('\n## Confusion Matrices\n\n')
        for name, m in results.items():
            cm = m['confusion_matrix']
            f.write(f'### {name}\n\n')
            f.write('```\n')
            f.write('                Predicted Unreliable  Predicted Reliable\n')
            f.write(f'Actual Unreliable      {cm[0][0]:<18}    {cm[0][1]}\n')
            f.write(f'Actual Reliable        {cm[1][0]:<18}    {cm[1][1]}\n')
            f.write('```\n\n')
            
        f.write('## Feature Importance (Top Positive and Negative N-grams)\n\n')
        vec = prod_pipeline.named_steps['tfidf']
        clf = prod_pipeline.named_steps['clf']
        feature_names = np.array(vec.get_feature_names_out())
        coefs = clf.coef_[0]
        
        top_reliable_idx = np.argsort(coefs)[-10:][::-1]
        top_unreliable_idx = np.argsort(coefs)[:10]
        
        f.write('### Indicative of Reliable Reporting (+ Coefficients)\n\n')
        for idx in top_reliable_idx:
            f.write(f'- **`{feature_names[idx]}`**: {coefs[idx]:+.4f}\n')
            
        f.write('\n### Indicative of Misleading / Sensational Reporting (- Coefficients)\n\n')
        for idx in top_unreliable_idx:
            f.write(f'- **`{feature_names[idx]}`**: {coefs[idx]:+.4f}\n')
            
        f.write('\n---\n*Generated during Model 3 training pipeline.*\n')
    
    print('Generated ml/evaluation/METRICS.md successfully')
    return results

if __name__ == '__main__':
    train_and_evaluate()
