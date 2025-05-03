import nltk
import os

def verify_nltk_resources():
    # List of all required NLTK resources
    required_resources = [
        'punkt',
        'stopwords',
        'averaged_perceptron_tagger',
        'wordnet',
        'omw-1.4'
    ]
    
    print("Verifying NLTK resources...")
    print(f"NLTK data path: {nltk.data.path}")
    
    for resource in required_resources:
        try:
            print(f"\nChecking {resource}...")
            nltk.data.find(f'tokenizers/{resource}')
            print(f"✓ {resource} is already installed")
        except LookupError:
            print(f"✗ {resource} not found. Downloading...")
            nltk.download(resource)
            print(f"✓ {resource} downloaded successfully")
    
    # Additional check for punkt specifically
    try:
        nltk.data.find('tokenizers/punkt')
        print("✓ punkt tokenizer is properly installed")
    except LookupError:
        print("✗ punkt tokenizer not found. Downloading...")
        nltk.download('punkt')
        print("✓ punkt tokenizer downloaded successfully")
    
    # Additional check for stopwords specifically
    try:
        nltk.data.find('corpora/stopwords')
        print("✓ stopwords are properly installed")
    except LookupError:
        print("✗ stopwords not found. Downloading...")
        nltk.download('stopwords')
        print("✓ stopwords downloaded successfully")

if __name__ == "__main__":
    verify_nltk_resources() 