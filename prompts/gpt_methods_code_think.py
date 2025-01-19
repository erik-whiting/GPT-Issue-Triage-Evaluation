from openai import OpenAI

from github_utils.github_methods import *

def describe_bot_role(repo, github_sha):
    bot_role_desc = f"""You are a maintainer of the
Biopython package. Your primary job is to triage new issues
reported by users. You may ask clarifying questions and make
troubleshooting suggesstions. Whenever possible, you should
also provide a git diff against the Biopython repository that 
fixes the reported issue. Not all issues will require code
changes, therefore a git diff is not a requirement. To make
git diffs, refer to the code repository at
https://github.com/erik-whiting/biopython. Think about whatever
response you provide systematically: will answers to your
clarifying questions make troubleshooting and issue resolution
easier? Will the provided diff really work? Are your suggestions
going to help the user figure out their problem? Also, here are the
file names and contents of some of the most updated Python
files in the project, this may assist in making diffs: {get_code_snippets(repo, github_sha)}"""
    return bot_role_desc.replace("\n", " ")


def generate_model(issue_data, repo, github_sha, model_type="gpt-4o-mini"):
    # Using gpt-4o-miini "With-Code-Context." That is, with
    # access to the 5 most updated .py files in the repo
    bot_role = describe_bot_role(repo, github_sha)
    if type(issue_data) == dict:
        pyv = issue_data["py_version"]
        bpv = issue_data["bp_version"]
        osv = issue_data["os_version"]
        aux_info = f"The user is on Python version {pyv}, Biopython version {bpv}, and operating system version {osv}."
        bot_role += f" {aux_info}"
        issue_data = "\n".join(issue_data["ticket_body"])
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
