from github import Github, Auth, UnknownObjectException


REPO_NAME = "biopython"
REPO_PATH = f"erik-whiting/{REPO_NAME}"


def authenticate():
    with open("../issue_reader_token") as fh:
        access_token = fh.read().strip()

    auth = Auth.Token(access_token)
    g = Github(auth=auth)

    return g


def get_repo(commit_sha=None):
    auth = authenticate()
    repo = auth.get_repo(REPO_PATH)
    if commit_sha:
        repo = repo.get_commit(commit_sha)
    return repo


def get_issues():
    repo = get_repo()
    issues = repo.get_issues()
    return issues


def get_issue(issue_num):
    repo = get_repo()
    issue = repo.get_issue(issue_num)
    return issue


def parse_issue(issue):
    issue_body = issue.body
    issue_data = issue_body.split("\n")
    parsed_data = {}
    # if issue_data[0] == "Setup":
    #     issue_data.pop(0)
    #     py_version = issue_data.pop(0).split(" ")[1].strip()
    #     bp_version = issue_data.pop(0).split(" ")[1].strip()
    #     os_version = issue_data.pop(0).split(": ")[1].strip()
    #     parsed_data = {"py_version": py_version, "bp_version": bp_version, "os_version": os_version}
    #     if issue_data[0] == "":
    #         issue_data.pop(0)
    #     parsed_data["ticket_body"] = issue_data
    if parsed_data:
        return parsed_data
    else:
        return issue_body


def get_files_with_most_commits(file_count_cutoff=5):
    with open("files_with_most_commits.txt") as fh:
        files = [line.strip() for line in fh.readlines()]
    files = [f for f in files if "Tests" not in f]
    files = [f for f in files if ".py" in f]
    files = [f for f in files if "__init__" not in f]
    files = [f.split("\t")[1] for f in files]
    return files[:file_count_cutoff]


def download_files(repo, git_sha=None):
    files = get_files_with_most_commits()
    file_code_map = {}
    for f in files:
        try:
            if git_sha:
                code = repo.get_contents(f, git_sha).decoded_content.decode("utf-8")
            else:
                code = repo.get_contents(f).decoded_content.decode("utf-8")
            file_code_map[f] = code
        except UnknownObjectException:
            continue
    return file_code_map


def get_code_snippets(repo, github_sha):
    code_map = download_files(repo, github_sha)
    code_snippet = ""
    for fname, code in code_map.items():
        code_snippet += f"File: {fname}\n{'-'*40}\n"
        code_snippet += f"{code}\n"
    return code_snippet


def issue_key(issue):
    return issue.title.replace(" ", "-") + f"-{issue.number}"


def mark_issue_checked(issue):
    with open("issues_checked.txt", "a") as fh:
        fh.write(f"{issue_key(issue)}\n")


def new_issues():
    with open("issues_checked.txt") as fh:
        old_issues = [i.strip() for i in fh.readlines()]
    new_issues = []
    for i in get_issues():
        key = issue_key(i)
        if key not in old_issues:
            new_issues.append(i)
    return new_issues
