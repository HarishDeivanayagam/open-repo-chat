Open Repo Chat
=============

Open Repo Chat is a developer-oriented tool that allows users to chat with a Git repository using natural language. This project leverages OpenAI's language models to interact with the Git repo, enabling developers to query, explore, and understand their codebase more efficiently.

Features
--------

*   **Chat with a Git Repository:** Ask questions about the codebase in natural language and get responses based on the repository's content.
*   **Code Navigation:** Simplifies code exploration by allowing developers to search for functions, variables, and logic within the repository.
*   **AI-Powered Assistance:** Uses OpenAI's API to process queries and generate accurate and contextual responses.
*   **Vector Store with Pinecone:** Utilizes Pinecone to store embeddings and efficiently search across large codebases.

Requirements
------------

To run the project, you will need:

1.  **OpenAI API Key:** For interacting with OpenAI's language model.
2.  **Pinecone API Key:** For using Pinecone's vector database to store and retrieve embeddings.

### Install Dependencies

1.  Clone the repository:
    
    bash
    
    Copy code
    
    `git clone https://github.com/harishdeivanayagam/open-repo-chat.git cd open-repo-chat`
    
2.  Install required Python packages:
    
    bash
    
    Copy code
    
    `pip install -r requirements.txt`
    
3.  Set up environment variables:
    
    *   Add your **OpenAI API key** and **Pinecone API key** in a `.env` file in the root directory:
        
        bash
        
        Copy code
        
        `OPENAI_API_KEY=your-openai-api-key PINECONE_API_KEY=your-pinecone-api-key PINECONE_INDEX=your-pinecone-index`
        

Usage
-----

1.  **Run the application:**
    
    bash
    
    Copy code
    
    `python main.py`
    
2.  **Interact with the Git repository:** Once the application is running, you can ask questions about the repository by typing natural language queries such as:
    
    *   "What does this function do?"
    *   "Where is the `main.py` file located?"
    *   "List all the classes in this repo."

Credits
-------

This project was created by **Harish Deivanayagam**.

License
-------

This project is licensed under the MIT License. See the LICENSE file for details.

* * *
