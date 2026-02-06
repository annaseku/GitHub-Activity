import requests
import json

def event_parser(event, n=1):
    """
    Takes a github Event and returns a string description of it.
    Takes an optional second argument n which specifies the number of times the same event has happened consecutively.
    :type n: int
    :type event: Event
    :rtype: str
    """

    multiple = True if n>1 else False
    article = str(n) if multiple else "a"
    plural = "s" if multiple else ""
    repo = event['repo']['name']
    action = event['payload']['action']
    event = event['type'][:-5].tolowerCase()

    if event == "commitcomment":
        return f"{action} {article} commit comment{plural} in {repo}"
    elif event == "create":
        type = event['payload']['ref_type']
        if multiple:
            ans = f"created {article} {type}"
            if type == "branch":
                ans = ans + "es"
            elif type == "tag":
                ans = ans + "s"
            elif type == "repository":
                ans = ans[:-1] + "ies"
            ans = ans + " in {repo}"
            return ans
        else:
            return f"created {article} {type} in {repo}"
    elif event == "delete":
        type = event['payload']['ref_type']
        if multiple:
            ans = f"created {article} {type}"
            if type == "branch":
                ans = ans + "es"
            elif type == "tag":
                ans = ans + "s"
            ans = ans + " in {repo}"
            return ans
        else:
            return f"created {article} {type} in {repo}"
    elif event == "discussion":
        return f"{action} {article} discussion{plural} in {repo}"
    elif event == "fork":
        return f"{action} {article} repositor{'ies' if multiple else "y"} in {repo}"
    elif event == "gollum":
        return f"created or updated {article} wiki page{plural} in {repo}"
    elif event == "issuecomment":
        return f"{action} {article} issue comment{plural} in {repo}"
    elif event == "issues":
        return f"{action} {article} issue{plural} in {repo}"
    elif event == "member":
        return f"{action} {article} collaborator{plural} to {repo}"
    elif event == "public":
        return f"made {repo} public"
    elif event == "pullrequest":
        return f"{action} {article} pull request{plural} in {repo}"
    elif event == "pullrequestreview":
        return f"{action} {article} pull request review{plural} in {repo}"
    elif event == "pullrequestreviewcomment":
        return f"{action} {article} pull request review comment{plural} in {repo}"
    elif event == "push":
        return f"pushed {article} commit{plural} to {repo}"
    elif event == "release":
        return f"published {article} release{plural} in {repo}"
    elif event == "watch":
        return f"starred {article} repositor{'ies' if multiple else "y"} in {repo}"


def main():

    username = input("Enter GitHub username: ")

    try:
        url = f'https://api.github.com/users/{username}/events'
        response = requests.get(url)
        response.raise_for_status()
    except ConnectionError:
        print("Failed to connect to GitHub API. Please check your internet connection.")
        return
    except requests.exceptions.HTTPError as err:
        status = err.response.status_code if err.response is not None else "unknown"
        if status == 403:
            print(f"Listing public events for {username}' is forbidden. Please try again with another user.")
        elif status == 304:
            print(f"No new events for {username}.")
        elif status == 503:
            print("Service is unavailable. Please try again later.")
        else:
            print(f"HTTP error occurred: {err}")
        return


    # formatted_json = json.dumps(response.json(), indent=4)
    # print(formatted_json)

    print("Recent activity for user:", username)
    for event in response.json():
        print("- " + event_parser(event))


if __name__ == "__main__":
    main()