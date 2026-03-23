import os
import pandas as pd
import joblib
import logging
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info("Starting ML model training...")
    
    # Check if the folder exists, if not, create it
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    
    # 1. Load dataset
    iris = load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names
    
    logging.info(f"Loaded Iris dataset with {X.shape[0]} samples and {X.shape[1]} features")
    
    # Save the dataset to CSV as sample dataset
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    df['target_name'] = df['target'].map(lambda idx: target_names[idx])
    
    csv_path = os.path.join(os.path.dirname(__file__), 'iris.csv')
    df.to_csv(csv_path, index=False)
    logging.info(f"Saved sample dataset to {csv_path}")
    
    # 2. Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Train model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # 4. Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Model trained successfully. Test Accuracy: {accuracy:.4f}")
    
    # 5. Save model
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    # Save a dictionary with the model and target names
    model_data = {
        'model': clf,
        'target_names': target_names,
        'feature_names': feature_names
    }
    joblib.dump(model_data, model_path)
    logging.info(f"Saved trained model to {model_path}")

if __name__ == '__main__':
    main()
