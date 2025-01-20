import pandas as pd
from openai import OpenAI
import openai.resources.embeddings as emb


def get_function_name(code):
    if code.startswith("def"):
        return code[len("def"):code.index("(")]


def get_until_no_space(all_lines, i):
    ret = [all_lines[i]]
    for j in range(i + 1, len(all_lines)):
        if len(all_lines[j]) == 0 or all_lines[j][0] in [" ", "\t", ")"]:
            ret.append(all_lines[j])
        else:
            break
    return "\n".join(ret)


def get_functions(filepath):
    with open(filepath, "r") as file:
        all_lines = file.read().replace("\r", "\n").split("\n")
        for i, l in enumerate(all_lines):
            for prefix in ["def ", "async def "]:
                if l.startswith(prefix):
                    code = get_until_no_space(all_lines, i)
                    function_name = get_function_name(code)
                    yield {
                        "code": code,
                        "function_name": function_name,
                        "filepath": filepath,
                    }
                    break


def extract_functions_from_repo(cutoff=100):
    with open("actual_files") as fh:
        files = [line.strip() for line in fh.readlines()]
    fpaths = []
    for f in files:
        fpaths.append(f)
        if len(fpaths) >= cutoff:
            break

    all_funcs = [f for fpath in fpaths for f in get_functions(fpath)]
    return all_funcs


def load_data():
    embedding_model = "text-embedding-ada-002"
    all_funcs = extract_functions_from_repo()
    df = pd.DataFrame(all_funcs)
    openai_client = OpenAI()
    embedder = emb.Embeddings(openai_client)
    df['code_embedding'] = df['code'].apply(lambda x: embedder.create(input=x, model=embedding_model))
    # df["code_embedding"] = df["function_name"].apply(lambda x: embedder.create(input=x, model=embedding_model))
    df["code_embedding"] = df["code_embedding"].apply(lambda x: x.data[0].embedding)
    df.to_csv("biopython_embeddings.csv", index=False)
    # df.to_csv("biopython_embeddings_function_name.csv", index=False)


load_data()
