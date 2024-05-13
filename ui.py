import os
import chainlit as cl
from rag_v1 import *

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None
 

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Summary Generator",
            markdown_description="Generate a summary of your project report",
        ),
        cl.ChatProfile(
            name="Q&A",
            markdown_description="Answer questions about your project report",
        ),

        cl.ChatProfile(
            name="Evidence Matrix Generator",
            markdown_description="Generate an evidence matrix for your project report",
        ),
    ]


@cl.on_chat_start
async def start():


    chat_profile = cl.user_session.get("chat_profile")
    if chat_profile == "Q&A":
        
        res = await cl.AskActionMessage(
            content="What kind of Q&A do you want to generate!",
            actions=[
                cl.Action(name="one", value="one", label="1️⃣ One file"),
                cl.Action(name="multi", value="multi", label="*️⃣ Multiple  Files"),
            ],
        ).send()

        if res and res.get("value") == "one":
            await cl.Message(content="Continue!").send()
            files = None
        
            # Wait for the user to upload a file
            while files == None:
                files = await cl.AskFileMessage(
                    content="Please upload a text file to begin!", accept=["application/pdf"]
                ).send()

            text_file = files[0]
            await cl.Message(content="Analysing your file, please wait..").send()
            print(text_file.path.split("/")[-1].replace(".pdf", ""))
            query_engine, llm, vector_index = rag_pipeline(setup_mode=True, 
                                                           collection_name=text_file.path.split("/")[-1].replace(".pdf", ""),
                                                           files = [text_file.path])
            
            cl.user_session.set("query_engine", query_engine)
            await cl.Message(content="All is ready! You can ask questions").send()
        elif res and res.get("value") == "multi":
            await cl.Message(content="Continue!").send()
            files = None
        
            # Wait for the user to upload a file
            while files == None:
                files = await cl.AskFileMessage(
                    content="Please upload multiple text files to begin!", accept=["application/pdf"]
                ).send()

            text_file = files[0]
            await cl.Message(content="Analysing your file, please wait..").send()
            print(text_file.path.split("/")[-1].replace(".pdf", ""))
            query_engine, llm, vector_index = rag_pipeline(setup_mode=True, 
                                                           collection_name=text_file.path.split("/")[-1].replace(".pdf", ""),
                                                           files = [text_file.path for text_file in files])
            
            cl.user_session.set("query_engine", query_engine)

    elif chat_profile == "Summary Generator":
        project = await cl.AskUserMessage(content="What is your project name?", timeout=10).send()
        
        questions = []
        collecting = True

        while collecting:
            # Ask for a question
            question = await cl.AskUserMessage(content="Please add a question for the report:", timeout=120).send()

            # Store the question
            questions.append(question)

            # Ask if the user wants to add more questions
            add_more = await cl.AskUserMessage(content="Do you want to add another question? (yes/no)", timeout=30).send()

            files = None
            print(add_more["output"])
            if add_more["output"].lower() != "yes":
                collecting = False

        # Wait for the user to upload a file
        while files == None:
            files = await cl.AskFileMessage(
                content="Please upload a text file to begin!", accept=["application/pdf"]
            ).send()

        text_file = files[0]
        await cl.Message(content="Analysing your file, please wait..").send()
        print(text_file.path.split("/")[-1].replace(".pdf", ""))
        query_engine, llm, vector_index = rag_pipeline(setup_mode=True, 
                                                        collection_name=text_file.path.split("/")[-1].replace(".pdf", ""),
                                                        files = [text_file.path])
        
        cl.user_session.set("query_engine", query_engine)
        await cl.Message(content="Generating Report, please wait..").send()

        query_engine = cl.user_session.get("query_engine")
        with open(project['output']+"_report.txt", "w") as file:
            for q in questions:
                 
                # Dummy function for generating answers, replace with your actual function
                res = await cl.make_async(query_engine.query)(MAIN_PROMPT + "\n\n" +q.get("output"))

                file.write(f"Question: {q.get("output")}\nAnswer: {str(res)}\n\n")

        # Send the report file to the user
        # elements = [cl.File(name=project['output']+"_report.txt", path="./"+project['output']+"_report.txt")]
        # await cl.Message(content="Here is your report", elements=elements).send()
        elements = [
            cl.File(
                name=project['output']+"_report.txt",
                path="./"+project['output']+"_report.txt",
                display="inline",
            ),
        ]

        await cl.Message(
            content="Here's your Summarized report", elements=elements
        ).send()


    elif chat_profile == "Evidence Matrix Generator":
        project = await cl.AskUserMessage(content="What is your project name?", timeout=10).send()
        
        questions = []
        collecting = True

        while collecting:
            # Ask for a question
            question = await cl.AskUserMessage(content="Please add a question for the report:", timeout=120).send()

            # Store the question
            questions.append(question)

            # Ask if the user wants to add more questions
            add_more = await cl.AskUserMessage(content="Do you want to add another question? (yes/no)", timeout=30).send()

            files = None
            print(add_more["output"])
            if add_more["output"].lower() != "yes":
                collecting = False

        # Wait for the user to upload a file
        while files == None:
            files = await cl.AskFileMessage(
                content="Please upload a text file to begin!", accept=["application/pdf"]
            ).send()

        text_file = files[0]
        await cl.Message(content="Analysing your file, please wait..").send()
        print(text_file.path.split("/")[-1].replace(".pdf", ""))
        query_engine, llm, vector_index = rag_pipeline(setup_mode=True, 
                                                        collection_name=text_file.path.split("/")[-1].replace(".pdf", ""),
                                                        files = [text_file.path])
        
        cl.user_session.set("query_engine", query_engine)
        await cl.Message(content="Generating Report, please wait..").send()

        query_engine = cl.user_session.get("query_engine")
        with open(project['output']+"_report.txt", "w") as file:
            for q in questions:
                 
                # Dummy function for generating answers, replace with your actual function
                res = await cl.make_async(query_engine.query)(MAIN_PROMPT + "\n\n" +q.get("output"))

                file.write(f"Question: {q.get("output")}\nAnswer: {str(res)}\n\n")

        # Send the report file to the user
        # elements = [cl.File(name=project['output']+"_report.txt", path="./"+project['output']+"_report.txt")]
        # await cl.Message(content="Here is your report", elements=elements).send()
        elements = [
            cl.File(
                name=project['output']+"_report.txt",
                path="./"+project['output']+"_report.txt",
                display="inline",
            ),
        ]

        await cl.Message(
            content="Here's your Evidence report for your judgement criteria", elements=elements
        ).send()

    # res = await cl.AskUserMessage(content="What is your project name?", timeout=10).send()
    # query_engine, llm, vector_index = rag_pipeline(setup_mode=False, collection_name=res['output'],file =json_file_path)
    # cl.user_session["query_engine"] = query_engine

@cl.on_message
async def main(message: cl.Message):
    print(message.content)
    
    msg = cl.Message(content="Thinking..", author="Assistant")
    await msg.send()

    query_engine = cl.user_session.get("query_engine") # type: RetrieverQueryEngine

    res = await cl.make_async(query_engine.query)(MAIN_PROMPT + "\n\n" +message.content)
    msg = cl.Message(content=str(res), author="Assistant")

    await msg.send()
