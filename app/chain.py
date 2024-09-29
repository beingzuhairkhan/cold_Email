import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import os
from langchain.globals import set_verbose

# Set the USER_AGENT environment variable
os.environ['GROQ_API_KEY']

# Set verbose logging for langchain
set_verbose(True)
# Ensure GROQ_API_KEY is available in environment variables
GROQ_API_KEY = os.environ['GROQ_API_KEY']

# Check if the API key is loaded
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables")

class Chain:
    def __init__(self):
        # Initialize the language model with specific parameters
        self.llm = ChatGroq(
            temperature=0, 
            model="llama-3.1-70b-versatile", 
            groq_api_key=GROQ_API_KEY
        )

    def extract_jobs(self, cleaned_text):
        # Ensure cleaned_text is a string
        if not isinstance(cleaned_text, str):
            raise TypeError(f"Expected cleaned_text to be str, got {type(cleaned_text)}")
          
        # Define a template for extracting job postings from text
        prompt_extract = PromptTemplate.from_template(
            """
            ## SCRAPED TEXT FROM WEBSITE:
            {page_data}

            The scraped text is from the career's page of a website.

            ### INSTRUCTION:

            Your job is to extract the job postings and return them in JSON format containing
            the following keys: 'role', 'experience', 'skills', and 'description'.

            Only return the valid JSON.

            ### VALID JSON (NO PREAMBLE):
            """
        )
        
        # Create the chain for extracting jobs by linking the prompt to the LLM
        chain_extract = prompt_extract | self.llm
        
        # Invoke the chain with the cleaned text
        print(f"Input to chain_extract: {cleaned_text}")
        res = chain_extract.invoke(input={'page_data': cleaned_text})
        
        try:
            # Parse the response into JSON format
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(res.content)
        except OutputParserException:
            # Handle cases where the response cannot be parsed
            raise OutputParserException("Context too big. Unable to parse jobs")    

        # Ensure the result is returned as a list of job objects
        return json_res if isinstance(json_res, list) else [json_res]

    def write_mail(self, job, links):
        # Ensure job and links are strings
        if not isinstance(job, str):
            raise TypeError(f"Expected job to be str, got {type(job)}")
        if not isinstance(links, str):
            # If links is a list, join it into a single string
            if isinstance(links, list):
                links = ", ".join(map(str, links))
            else:
                raise TypeError(f"Expected links to be str or list, got {type(links)}")

        # Define a template for generating a cold email based on job description
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:

            {job_description}

            ### INSTRUCTION:

            You are Zuhair, a business development executive at AtliQ. AtliQ is an AI & Software Consulting firm specializing 
            in the seamless integration of business processes through automated tools. Over our experience, we have empowered 
            numerous enterprises with tailored solutions, fostering process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above, emphasizing how AtliQ can help in fulfilling 
            their needs.

            Also, add the most relevant ones from the following links to showcase AtliQ's portfolio. Remember you are Zuhair, BDE at Atliq.

            ### EMAIL (NO PREAMBLE):
            """
        )

        # Create the chain for generating emails by linking the prompt to the LLM
        chain_mail = prompt_email | self.llm
        
        # Debugging input values
        print(f"Job description input: {job}")
        print(f"Links input: {links}")

        # Invoke the chain with job details and portfolio links
        res = chain_mail.invoke({"job_description": str(job), "link_list": links})
        
        # Return the generated email content
        return res.content
