import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_resources():
    resources = [
        'punkt_tab',
        'punkt', 
        'averaged_perceptron_tagger_eng',
        'averaged_perceptron_tagger',
        'wordnet',
        'stopwords'
    ]
    
    print("Downloading NLTK resources...")
    
    for resource in resources:
        try:
            print(f"Downloading {resource}...")
            nltk.download(resource, quiet=False)
            print(f"✓ {resource} downloaded successfully")
        except Exception as e:
            print(f"✗ Failed to download {resource}: {e}")
    
    print("\nTesting tokenization...")
    try:
        from nltk.tokenize import sent_tokenize, word_tokenize
        from nltk.tag import pos_tag
        
        test_text = "This is a test. It should work now."
        sentences = sent_tokenize(test_text)
        words = word_tokenize(sentences[0])
        tags = pos_tag(words)
        
        print(f"✓ Sentences: {sentences}")
        print(f"✓ Words: {words}")
        print(f"✓ POS tags: {tags}")
        print("\nNLTK setup complete!")
        
    except Exception as e:
        print(f"✗ Testing failed: {e}")
        print("Using fallback methods...")

if __name__ == "__main__":
    download_nltk_resources()