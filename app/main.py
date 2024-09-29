import streamlit as st 
from chain import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader

def flatten_links(nested_links):
    # Flatten the nested list of dictionaries to get a flat list of strings
         return [link['links'] for sublist in nested_links for link in sublist]



def create_streamlit_app(llm, portfolio):
    st.title("Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-37999")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            # Load the webpage content
            page_content = loader.load().pop().page_content
            
            # Clean the loaded text
            cleaned_text = clean_text(page_content)

            # Load the portfolio into the ChromaDB collection
            portfolio.load_portfolio()
            
            # Extract job details from the cleaned data
            jobs = llm.extract_jobs(cleaned_text)
            
            # Iterate through extracted jobs
            for job in jobs:
                job_description = job.get('description', '')
                skills = job.get('skills', [])

                # Generate the links using the flattened links
                links = portfolio.query_links(skills)
                
                # Flatten the links to a list of strings
                flat_links = flatten_links(links)

                # Check that flat_links is not empty before generating the email
                if flat_links:
                    email = llm.write_mail(job_description, flat_links)
                    # Display the generated email in the Streamlit app
                    st.code(email, language="markdown")
                else:
                    st.warning(f"No links found for skills: {skills}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="✉️")
    create_streamlit_app(chain, portfolio)