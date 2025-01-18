from github import Github, Auth


REPO_NAME = "biopython"
REPO_PATH = f"erik-whiting/{REPO_NAME}"


def authenticate():
    with open("../issue_reader_token") as fh:
        access_token = fh.read().strip()

    auth = Auth.Token(access_token)
    g = Github(auth=auth)

    return g


def get_repo():
    auth = authenticate()
    repo = auth.get_repo(REPO_PATH)
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
    if issue_data[0] == "Setup":
        issue_data.pop(0)
        py_version = issue_data.pop(0).split(" ")[1].strip()
        bp_version = issue_data.pop(0).split(" ")[1].strip()
        os_version = issue_data.pop(0).split(": ")[1].strip()
        parsed_data = {"py_version": py_version, "bp_version": bp_version, "os_version": os_version}
        if issue_data[0] == "":
            issue_data.pop(0)
        parsed_data["ticket_body"] = issue_data
    if parsed_data:
        return parsed_data
    else:
        return issue_body


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
