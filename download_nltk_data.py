import nltk

def download_nltk_data():
    print("Downloading required NLTK data...")
    
    # List of required NLTK data
    required_data = [
        'punkt',
        'stopwords',
        'averaged_perceptron_tagger',
        'wordnet',
        'omw-1.4'
    ]
    
    for data in required_data:
        try:
            print(f"Checking {data}...")
            nltk.data.find(f'tokenizers/{data}')
            print(f"{data} already downloaded")
        except LookupError:
            print(f"Downloading {data}...")
            nltk.download(data)
            print(f"{data} downloaded successfully")
    
    print("\nAll required NLTK data has been downloaded successfully!")

if __name__ == "__main__":
    download_nltk_data() 