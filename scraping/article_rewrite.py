from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Load T5 model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")

def paraphrase_sentence(sentence, max_length=256):
    input_text = f"paraphrase: {sentence} </s>"
    inputs = tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=max_length)

    outputs = model.generate(
        inputs,
        max_length=max_length,
        num_beams=5,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def article_rewriter(text):
    sentences = sent_tokenize(text)
    rewritten_sentences = [paraphrase_sentence(sent) for sent in sentences]
    print(rewritten_sentences)
    return ' '.join(rewritten_sentences)

# Example usage
input_text = "The quick brown fox jumps over the lazy dog. It was a bright sunny day in the meadow."
rewritten_text = article_rewriter(input_text)

print("Original:", input_text)
print("Rewritten:", rewritten_text)
