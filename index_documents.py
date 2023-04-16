import os
import sys
import shutil
import json
import gradio as gr
from dotenv import load_dotenv
from llama_index import (
    SimpleDirectoryReader,
    GPTListIndex,
    GPTSimpleVectorIndex,
    LLMPredictor,
    PromptHelper,
    ServiceContext,
)
from llama_index.node_parser import SimpleNodeParser
from langchain import OpenAI
import base64
from pathlib import Path

# Load environment variables from .env file
load_dotenv()
# Get the value of OPENAI_API_KEY from the environment
api_key = os.getenv("OPENAI_API_KEY")
# Use the API key in your code
os.environ["OPENAI_API_KEY"] = api_key

sys.path.append("/my_functions")

# Defining the parameters for the index
max_input_size = 4096
num_outputs = 1024
max_chunk_overlap = 20

prompt_helper = PromptHelper(
    max_input_size,
    num_outputs,
    max_chunk_overlap,
)

llm_predictor = LLMPredictor(
    llm=OpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs)
)

service_context = ServiceContext.from_defaults(
    llm_predictor=llm_predictor, prompt_helper=prompt_helper
)


def save_uploaded_files(uploaded_files):
    file_paths = []
    script_directory = os.path.dirname(os.path.realpath(__file__))
    docs_folder = os.path.join(script_directory, "docs")

    for uploaded_file in uploaded_files:
        full_path = uploaded_file.name
        print(full_path)
        filename = os.path.basename(full_path)
        file_path = os.path.join(docs_folder, filename)

        # Debugging: check the file size, name, and contents
        uploaded_file.seek(0, os.SEEK_END)
        file_size = uploaded_file.tell()
        uploaded_file.seek(0)
        file_contents = uploaded_file.read()

        # Save the uploaded file to the destination
        with open(file_path, "wb") as f:
            uploaded_file.seek(0)
            f.write(file_contents)

        file_paths.append(file_path)
    return file_paths


def construct_index(directory_path):
    if os.path.isfile("index.json"):
        # Index file exists, so we'll load it and add new documents to it
        index = GPTSimpleVectorIndex.load_from_disk(
            "index.json", service_context=service_context
        )
        documents = SimpleDirectoryReader(directory_path).load_data()
        doc_summaries = {}
        for doc in documents:
            summary = input(f"Enter a summary for {doc.doc_id}: ")
            doc_summaries[doc.doc_id] = summary
            index.insert(doc, service_context=service_context)
        index.save_to_disk("index.json")
    else:
        # Index file doesn't exist, so we'll create a new index from scratch
        documents = SimpleDirectoryReader(directory_path).load_data()
        index = GPTSimpleVectorIndex.from_documents(
            documents, service_context=service_context
        )
        index.save_to_disk("index.json")

    # Define the paths to the source and destination folders
    absolute_path = os.path.dirname(__file__)
    src_folder = os.path.join(absolute_path, "docs/")
    dest_folder = os.path.join(absolute_path, "indexed_documents/")

    # Get a list of all the files in the source folder
    files = os.listdir(src_folder)

    # Move each file from the source folder to the destination folder,
    # except for the "do_not_delete.txt" file
    for file in files:
        if file != "do_not_delete.txt":
            src_path = os.path.join(src_folder, file)
            dest_path = os.path.join(dest_folder, file)
            shutil.move(src_path, dest_path)

    return index


def process_files_and_index(uploaded_files):
    print("Uploaded files:")
    for file in uploaded_files:
        print(f"Filename: {file.name}")
        print(f"Contents: {file.read()}")
    if uploaded_files:
        save_uploaded_files(uploaded_files)
        # construct_index("docs")

        return "Documents successfully indexed."
    else:
        return "No files uploaded."


upload_and_index_interface = gr.Interface(
    fn=process_files_and_index,
    inputs=gr.File(file_count="multiple", label="Upload your files"),
    outputs="text",
    title="Upload and Index Documents",
)

if __name__ == "__main__":
    upload_and_index_interface.launch()
