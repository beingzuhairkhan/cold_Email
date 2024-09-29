import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path='my_portfolio.csv'):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if self.collection.count() == 0:  # Check if the collection is empty
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],  # `documents` expects a list
                    metadatas=[{"links": row["Links"]}],  # `metadatas` expects a list of dictionaries
                    ids=[str(uuid.uuid4())]  # Each ID should be unique and in a list
                )
    
    def query_links(self, skills):
        # Ensure skills are in the correct format
        if isinstance(skills, list):
            skills = [skill for skill in skills if isinstance(skill, str)]  # Filter out non-string skills
        else:
            raise ValueError("Skills must be a list of strings.")

        # Run a query against the collection using the skills provided
        result = self.collection.query(
            query_texts=skills,  # `query_texts` should be a list of strings
            n_results=2
        )
        return result.get('metadatas', [])
    
