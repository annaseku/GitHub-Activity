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
    action = event['payload']['action'] if 'payload' in event and 'action' in event['payload'] else None
    event_str = event['type'][:-5].lower()

    if event_str == "commitcomment":
        return f"{action} {article} commit comment{plural} in {repo}"
    elif event_str == "create":
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
    elif event_str == "delete":
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
    elif event_str == "discussion":
        return f"{action} {article} discussion{plural} in {repo}"
    elif event_str == "fork":
        return f"{action} {article} repositor{'ies' if multiple else 'y'} in {repo}"
    elif event_str == "gollum":
        return f"created or updated {article} wiki page{plural} in {repo}"
    elif event_str == "issuecomment":
        return f"{action} {article} issue comment{plural} in {repo}"
    elif event_str == "issues":
        return f"{action} {article} issue{plural} in {repo}"
    elif event_str == "member":
        return f"{action} {article} collaborator{plural} to {repo}"
    elif event_str == "public":
        return f"made {repo} public"
    elif event_str == "pullrequest":
        return f"{action} {article} pull request{plural} in {repo}"
    elif event_str == "pullrequestreview":
        return f"{action} {article} pull request review{plural} in {repo}"
    elif event_str == "pullrequestreviewcomment":
        return f"{action} {article} pull request review comment{plural} in {repo}"
    elif event_str == "push":
        return f"pushed {article} commit{plural} to {repo}"
    elif event_str == "release":
        return f"published {article} release{plural} in {repo}"
    elif event_str == "watch":
        return f"starred {article} repositor{'ies' if multiple else 'y'} in {repo}"


def is_same_event(event1, event2):
    """
    Takes two github events and returns true if they are the same type of event in the same repository, false otherwise.
    :type event1: Event
    :type event2: Event
    :rtype: bool
    """
    return event1['type'] == event2['type'] and event1['repo']['name'] == event2['repo']['name']


def main():
    """
    CLI that prompts the user for a GitHub username and lists their recent activity.
    Groups consecutive events of the same type in the same repository together and showing the count of how many
    times that event happened in a row.
    """

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

    print("Recent activity for user:", username)
    last_event = response.json()[0]
    last_event_count = 1
    for event in response.json()[1:]:
        # count how many times the same event has happened in a row
        if last_event:
            if is_same_event(last_event, event):
                last_event_same = True
                last_event_count += 1
                continue

        # print events and consecutive frequency, producing output and resetting the count once a new event is seen
        if not is_same_event(event, last_event):
            print("- " + event_parser(last_event, last_event_count))
            if last_event_count > 1:
                last_event_count = 1

        last_event = event

if __name__ == "__main__":
    main()