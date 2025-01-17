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
