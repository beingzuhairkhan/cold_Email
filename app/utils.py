import re

def clean_text(text):
    # Check if the input is a string
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Remove HTML tags
    text = re.sub('<[^>]*?>', '', text)
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove special characters (only keep letters and numbers)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    
    # Trim leading and trailing whitespace
    text = text.strip()
    
    # Remove extra whitespace within the text
    text = ' '.join(text.split())
    
    return text