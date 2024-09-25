from openai import OpenAI
import os
import git
from pinecone import Pinecone
from tools import tools_data
import json

class Agent:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.repo = git.Repo(self.folder_path)
        self.openai = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG_ID")
        )
        self.last_indexed_commit = ""
        self.current_branch = ""
        self.messages = [
            {
                "role": "system",
                "content": "You are a full stack app developer"
            }
        ]

        self.pc = Pinecone(
            api_key=os.getenv("PINECONE_API_KEY")
        )

        self.pc_index = self.pc.Index(os.getenv("PINECONE_INDEX"))

    def switch_branch(self, branch_name):
        
        branches = [head.name for head in self.repo.heads]

        if branch_name in branches:
            # If the branch exists, checkout to it
            print(f"Switching to existing branch '{branch_name}'")
            self.repo.git.checkout(branch_name)
        else:
            # If the branch doesn't exist, create and checkout to it
            print(f"Branch '{branch_name}' doesn't exist. Creating and switching to it.")
            self.repo.git.checkout('-b', branch_name)


    # Search the web for docs
    def _search_web(self, query):
        pass



    # Index the repository by comparing the hash
    def _index_code(self):
        if self.last_indexed_commit != self.repo.commit("HEAD").hexsha:

            # index the code
            files = self.repo.git.ls_files().splitlines()
            
            for file_name in files:
                try:
                    file = open(os.path.join(self.folder_path, file_name), "r")
                    file_contents = file.read()

                    # get embedding
                    embeddings = self.openai.embeddings.create(
                        model="text-embedding-3-small",
                        input=file_contents
                    )

                    embeddings = embeddings.data[0].embedding

                    # add to pinecone
                    self.pc_index.upsert(
                        vectors=[
                            {
                                "id": file_name,
                                "values": embeddings,
                                "metadata": {
                                    "filename": file_name
                                }
                            }
                        ]
                    )

                    file.close()
                
                except Exception as e:
                    print(f"Unable to index file: {file_name}")

            self.last_indexed_commit = self.repo.commit("HEAD").hexsha



    def _search_files(self, query):
        # Make query to pinecone and find the supporting files
        embedding = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )

        embedding = embedding.data[0].embedding

        results = self.pc_index.query(
            vector=embedding,
            top_k=3
        )

        results = results["matches"]

        output = ""

        for result in results:

            file_contents = ""

            with open(os.path.join(self.folder_path, result["id"]), 'r') as file:
                for line_number, line in enumerate(file, start=1):
                    file_contents += f"{line_number}: {line.strip()}"

            output += f"The file contents of {result["id"]}: {file_contents}\n"

        return output

    def update_file(self, file_path, start_position, end_position, data, commit_message):
        
        start_position = int(start_position)
        end_position = int(end_position)

        file = open(os.path.join(self.folder_path, file_path), 'w')

        file_content = file.read()

        file_content = file_content[:start_position] + data + file_content[end_position:]
        file.close()

        self.repo.git.add(file_path)
        self.repo.index.commit(commit_message)

        return "File commited successfully"


    # Ask the user for a query
    def ask(self, query):

        self._index_code()

        self.messages.append({
            "role": "user",
            "content": f"Based on the user's query, answer the following question: {query}"
        })

        while True:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=self.messages,
                tools=tools_data,
                parallel_tool_calls=False
            )

            self.messages.append(response.choices[0].message)

            tools = response.choices[0].message.tool_calls

            if tools is None or len(tools) < 1:
                break

            function_name = tools[0].function.name
            function_args = json.loads(tools[0].function.arguments)

            if function_name == "search_files":
                data = self._search_files(function_args["query"])

            self.messages.append({
                "role": "tool",
                "content": data,
                "tool_call_id": tools[0].id
            })


        return response.choices[0].message.content
