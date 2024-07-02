from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the Sentence-Transformers model
model = SentenceTransformer('nickmuchi/setfit-finetuned-financial-text-classification')

# Example compared sentence and group of sentences
compared_sentence = ".Net django"
group_of_sentences = [
    ".Net django",
    ".Net django laravel python",
    ".Net django laravel python c#",
    ".Net django laravel python c# java script"
]

# Tokenize and encode the compared sentence
compared_sentence_embedding = model.encode([compared_sentence])[0]

# Calculate cosine similarity for each sentence in the group
similarities = []
for sentence in group_of_sentences:
    sentence_embedding = model.encode([sentence])[0]
    
    # Normalize the vectors
    compared_sentence_embedding_normalized = compared_sentence_embedding / np.linalg.norm(compared_sentence_embedding)
    sentence_embedding_normalized = sentence_embedding / np.linalg.norm(sentence_embedding)
    
    # Calculate cosine similarity
    similarity = np.dot(compared_sentence_embedding_normalized, sentence_embedding_normalized)
    similarities.append(similarity)

# Print similarities
for sentence, similarity in zip(group_of_sentences, similarities):
    print(f"Sentence: '{sentence}' - Similarity: {similarity}")
