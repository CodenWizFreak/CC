import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from collections import defaultdict

nltk.download('punkt_tab')
def download_nltk_data():
    resources = [
        ('punkt_tab', 'tokenizers/punkt_tab'),
        ('punkt', 'tokenizers/punkt'),
        ('averaged_perceptron_tagger_eng', 'taggers/averaged_perceptron_tagger_eng'),
        ('averaged_perceptron_tagger', 'taggers/averaged_perceptron_tagger')
    ]
    
    for resource, path in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except:
                continue

download_nltk_data()

class TextProcessor:
    def __init__(self):
        self.verbs = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
        self.nouns = {'NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP', 'PRP$', 'WP', 'WP$'}
    
    def extract_svo_triplets(self, sentence):
        try:
            tokens = word_tokenize(sentence.lower())
            pos_tags = pos_tag(tokens)
        except:
            tokens = sentence.lower().split()
            pos_tags = [(token, 'NN') for token in tokens]
        
        triplets = []
        
        subj_candidates = self._find_subjects(pos_tags)
        verb_candidates = self._find_verbs(pos_tags)
        obj_candidates = self._find_objects(pos_tags)
        
        for subj in subj_candidates:
            for verb in verb_candidates:
                for obj in obj_candidates:
                    if subj != obj:
                        triplets.append((subj, verb, obj))
        
        if not triplets:
            triplets = self._simple_extraction(pos_tags)
            
        return triplets[:3]
    
    def _find_subjects(self, pos_tags):
        subjects = []
        for i, (word, tag) in enumerate(pos_tags):
            if tag in self.nouns and i < len(pos_tags) // 2:
                subjects.append(word)
        return subjects[:2] if subjects else ['subject']
    
    def _find_verbs(self, pos_tags):
        verbs = []
        for word, tag in pos_tags:
            if tag in self.verbs:
                verbs.append(word)
        return verbs[:2] if verbs else ['relates']
    
    def _find_objects(self, pos_tags):
        objects = []
        for i, (word, tag) in enumerate(pos_tags):
            if tag in self.nouns and i > len(pos_tags) // 2:
                objects.append(word)
        return objects[:2] if objects else ['object']
    
    def _simple_extraction(self, pos_tags):
        words = [word for word, tag in pos_tags if tag in self.nouns or tag in self.verbs]
        
        if len(words) >= 3:
            return [(words[0], words[1], words[2])]
        elif len(words) == 2:
            return [(words[0], 'relates', words[1])]
        elif len(words) == 1:
            return [(words[0], 'exists', 'entity')]
        else:
            return [('subject', 'relates', 'object')]
    
    def clean_text(self, text):
        text = re.sub(r'[^\w\s\.\!\?]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def get_sentence_entities(self, sentence):
        try:
            tokens = word_tokenize(sentence)
            pos_tags = pos_tag(tokens)
        except:
            tokens = sentence.split()
            pos_tags = [(token, 'NN') for token in tokens]
        
        entities = []
        for word, tag in pos_tags:
            if tag in self.nouns:
                entities.append(word.lower())
                
        return list(set(entities))
    
    def compute_sentence_similarity(self, sent1, sent2):
        entities1 = set(self.get_sentence_entities(sent1))
        entities2 = set(self.get_sentence_entities(sent2))
        
        if not entities1 or not entities2:
            return 0.0
            
        intersection = len(entities1 & entities2)
        union = len(entities1 | entities2)
        
        return intersection / union if union > 0 else 0.0
        
    def extract_sentences(self, text):
        text = re.sub(r'\s+', ' ', text.strip())
        
        try:
            from nltk.tokenize import sent_tokenize
            sentences = sent_tokenize(text)
        except:
            sentences = self._fallback_sentence_split(text)
        
        return [s.strip() for s in sentences if len(s.strip()) > 5]
    
    def _fallback_sentence_split(self, text):
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def extract_svo_triplets(self, sentence):
        tokens = word_tokenize(sentence.lower())
        pos_tags = pos_tag(tokens)
        
        triplets = []
        
        subj_candidates = self._find_subjects(pos_tags)
        verb_candidates = self._find_verbs(pos_tags)
        obj_candidates = self._find_objects(pos_tags)
        
        for subj in subj_candidates:
            for verb in verb_candidates:
                for obj in obj_candidates:
                    if subj != obj:
                        triplets.append((subj, verb, obj))
        
        if not triplets:
            triplets = self._simple_extraction(pos_tags)
            
        return triplets[:3]
    
    def _find_subjects(self, pos_tags):
        subjects = []
        for i, (word, tag) in enumerate(pos_tags):
            if tag in self.nouns and i < len(pos_tags) // 2:
                subjects.append(word)
        return subjects[:2] if subjects else ['subject']
    
    def _find_verbs(self, pos_tags):
        verbs = []
        for word, tag in pos_tags:
            if tag in self.verbs:
                verbs.append(word)
        return verbs[:2] if verbs else ['relates']
    
    def _find_objects(self, pos_tags):
        objects = []
        for i, (word, tag) in enumerate(pos_tags):
            if tag in self.nouns and i > len(pos_tags) // 2:
                objects.append(word)
        return objects[:2] if objects else ['object']
    
    def _simple_extraction(self, pos_tags):
        words = [word for word, tag in pos_tags if tag in self.nouns or tag in self.verbs]
        
        if len(words) >= 3:
            return [(words[0], words[1], words[2])]
        elif len(words) == 2:
            return [(words[0], 'relates', words[1])]
        elif len(words) == 1:
            return [(words[0], 'exists', 'entity')]
        else:
            return [('subject', 'relates', 'object')]
    
    def clean_text(self, text):
        text = re.sub(r'[^\w\s\.\!\?]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def get_sentence_entities(self, sentence):
        tokens = word_tokenize(sentence)
        pos_tags = pos_tag(tokens)
        
        entities = []
        for word, tag in pos_tags:
            if tag in self.nouns:
                entities.append(word.lower())
                
        return list(set(entities))
    
    def compute_sentence_similarity(self, sent1, sent2):
        entities1 = set(self.get_sentence_entities(sent1))
        entities2 = set(self.get_sentence_entities(sent2))
        
        if not entities1 or not entities2:
            return 0.0
            
        intersection = len(entities1 & entities2)
        union = len(entities1 | entities2)
        
        return intersection / union if union > 0 else 0.0