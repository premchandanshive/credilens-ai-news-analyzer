"""
CrediLens — Model Evaluation Utility
Loads a trained pipeline and runs comprehensive performance evaluation.
"""

import os
import csv
import joblib
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def evaluate(model_path='ml/saved_models/tfidf_logreg_credilens.joblib', data_path='ml/datasets/sample_news.csv'):
    if not os.path.exists(model_path):
        print(f"Model artifact not found at {model_path}. Run train_baselines.py first.")
        return
        
    model = joblib.load(model_path)
    
    texts = []
    labels = []
    with open(data_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            combined = (row.get('title') or '') + ' ' + (row.get('text') or '')
            texts.append(combined)
            labels.append(1 if row.get('label') == 'reliable' else 0)
            
    X = np.array(texts)
    y = np.array(labels)
    
    y_pred = model.predict(X)
    
    print('=== CrediLens Model Evaluation Report ===')
    print(f'Accuracy: {accuracy_score(y, y_pred):.4f}\n')
    print('Classification Report:')
    print(classification_report(y, y_pred, target_names=['Unreliable', 'Reliable'], digits=4))
    print('Confusion Matrix:')
    print(confusion_matrix(y, y_pred))

if __name__ == '__main__':
    evaluate()
