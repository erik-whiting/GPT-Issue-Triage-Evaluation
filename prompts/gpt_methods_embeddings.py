from openai import OpenAI
import numpy as np
import pandas as pd


def describe_bot_role():
    bot_role_desc = """You are a maintainer of the
Biopython package. Your primary job is to triage new issues
reported by users. You may ask clarifying questions and make
troubleshooting suggesstions. Whenever possible, you should
also provide a git diff against the Biopython repository that 
fixes the reported issue. Not all issues will require code
changes, therefore a git diff is not a requirement.
To make git diffs, refer to the code repository at
https://github.com/erik-whiting/biopython."""
    return bot_role_desc.replace("\n", " ")


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_embedding(text, model="text-embedding-ada-002"):
    client = OpenAI()
    return client.embeddings.create(input = [text], model=model).data[0].embedding


def read_embeddings_file():
    df = pd.read_csv('../embeddings_tools/biopython_embeddings.csv')
    df['code_embedding'] = df.code_embedding.apply(eval).apply(np.array)
    return df


def search_functions(df, code_query, n=5):
    question_embedding = get_embedding(code_query, model="text-embedding-ada-002")
    question_embedding = np.array(question_embedding)
    df['similarities'] = df.code_embedding.apply(lambda x: cosine_similarity(x, question_embedding))
    res = df.sort_values('similarities', ascending=False).head(n)
    return res


def code_result_suggestions(search_results):
    response = "\nHere are some functions that may be relevant to the issue:\n"
    for i, row in search_results.iterrows():
        response += f"Function {i + 1}:\nCode: {row['code']}\nSimilarity Score: {row['similarities']:.4f}\n\n"
    return response


def generate_model(issue_data, model_type="gpt-4o-mini"):
    # Using gpt-4o-miini "code embeddings"
    bot_role = describe_bot_role()
    if type(issue_data) == dict:
        pyv = issue_data["py_version"]
        bpv = issue_data["bp_version"]
        osv = issue_data["os_version"]
        aux_info = f"The user is on Python version {pyv}, Biopython version {bpv}, and operating system version {osv}."
        bot_role += f" {aux_info}"
        issue_data = "\n".join(issue_data["ticket_body"])
    embeddings_df = read_embeddings_file()
    search_results = search_functions(embeddings_df, issue_data)
    code_result_message = code_result_suggestions(search_results)
    issue_data += code_result_message
    client = OpenAI()
    model = client.chat.completions.create(
        model=model_type,
        messages=[
            {
                "role": "developer",
                "content": bot_role
            },
            {
                "role": "user",
                "content": issue_data
            }
        ]
    )

    # Response is in model.choices[0].message.content
    return model
