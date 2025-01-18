from openai import OpenAI


def describe_bot_role():
    bot_role_desc = """You are a maintainer of the
Biopython package. Your primary job is to triage new issues
reported by users. You may ask clarifying questions and make
troubleshooting suggesstions. Whenever possible, you should
also provide a git diff against the Biopython repository that 
fixes the reported issue. The Biopython code can be found
at https://github.com/erik-whiting/biopython."""
    return bot_role_desc.replace("\n", " ")


def generate_model(issue_data, model_type="gpt-4o-mini"):
    # Using gpt-4o-miini "out of the box." That is,
    # with no fine tuning or fine tuning.
    bot_role = describe_bot_role()
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
