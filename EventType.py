from enum import Enum

class EventType(Enum):
    # an enum to store the strings associated with each github event
    COMMITCOMMENTEVENT = "a commit comment in"
    CREATEEVENT = "Branch or tag created in"
    DELETEEVENT = "Branch or tag deleted in"
    DISCUSSIONEVENT = "a discussion in"
    FORKEVENT = "the repository"
    ISSUECOMMENTEVENT = "Issue comment created in"
    MEMBEREVENT = 'Added a collaborator to or from'
    PUBLICEVENT = "Made public the repository"
    PULLREQUESTREVIEWCOMMENTEVENT = "Created a pull request review comment in"
    PUSHEVENT = "Pushed a commit to"
    RELEASEEVENT = "Published a release in"
    WATCHEVENT = "Starred the repository"

    # multi-action events
    GOLLUMEVENT = "a wiki page in"
    ISSUESEVENT = "an issue in"
    PULLREQUESTEVENT = "a pull request in"
    PULLREQUESTREVIEWEVENT = "a pull request review in"

    def message(self):
        return self.value