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


def generate_model_response(issue_text, output_path, model_type="gpt-4o-mini"):
    # Using gpt-4o-miini "out of the box." That is,
    # with no fine tuning or auxiliary information.
    client = OpenAI()
    model = client.chat.completions.create(
        model = model_type,
        messages=[
            {
                "role": "developer",
                "content": describe_bot_role()
            },
            {"role": "user", "content": issue_text}
        ]
    )

    with open(output_path, "w") as fh:
        fh.write(model.choices[0].message.content)

    return model
