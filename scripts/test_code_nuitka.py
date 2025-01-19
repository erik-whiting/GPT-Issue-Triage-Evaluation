import github_utils.github_methods as gm
import prompts.gpt_methods_code as gpt_wc


pre_fix_sha = "6ebae6a66d2f313eaec94c2cb10e25ed5d2eae75"

model_under_test = "With-Code-Context"
nuitka_issue = 20

repo = gm.get_repo()
issue = repo.get_issue(nuitka_issue)

issue_text = gm.parse_issue(issue)

model = gpt_wc.generate_model(issue_text, repo, pre_fix_sha)
response = model.choices[0].message.content
response += f"\n\n{'-'*50}\n\n"
response += f"This test-response generated by model version *{model_under_test}*"
issue.create_comment(response)

print("Done")
