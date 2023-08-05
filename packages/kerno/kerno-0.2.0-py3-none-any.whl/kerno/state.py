"""Classes that store state."""

from datetime import datetime


class UIMessage:
    """Represents a message to be displayed to the user in the UI."""

    KINDS = ['danger', 'warning', 'info', 'success']

    def __init__(self, title, kind='success', plain=None, html=None):
        """Constructor.

        ``kind`` must be one of ('danger', 'warning', 'info', 'success').
        """
        args_are_valid = (plain and not html) or (html and not plain)
        assert args_are_valid
        if kind == 'error':
            kind = 'danger'
        assert kind in self.KINDS, 'Unknown kind of message: "{0}". ' \
            "Possible kinds are {1}".format(kind, self.KINDS)
        self.title = title
        self.plain = plain
        self.html = html

    def __repr__(self):
        return '<{} "{}">'.format(self.__class__.__name__, self.title)

    def to_dict(self):
        """Convert instance to a dictionary, usually for JSON output."""
        return self.__dict__.copy()


class Peto:
    """State bag for an operation in progress.

    It's the same as a *request* in a web framework. In Kerno, each
    action in an operation may modify the *peto*. This is how an action
    sends data to the next action.
    """

    def __init__(self, kerno, user, operation, payload: dict, when=None, **kw):
        """Constructor.

        ``kerno`` must be the Kerno instance for the current application.
        ``user`` is the User instance requesting the current operation.
        ``operation`` is the activity being requested by the user.
        ``payload`` is a dictionary containing the operation parameters.
        """
        self.kerno = kerno
        self.when = when or datetime.utcnow()
        self.user = user      # the user or component requesting this action
        self.operation = operation
        self.dirty = payload  # dictionary containing the action parameters
        self.clean = None     # validation converts ``dirty`` to ``clean``
        self.rezulto = Rezulto()
        for key, val in kw.items():
            setattr(self, key, val)


class Returnable:
    """Base class for Rezulto and for MalbonaRezulto.

    Subclasses MUST define a ``status_int`` variable and a DEFAULT_KIND.
    """

    def __init__(self):
        self.messages = []  # Grave messages for the user to read
        self.toasts = []    # Quick messages that disappear automatically
        self.debug = {}     # Not displayed to the user
        self.redirect = None  # URL to redirect to

    def __repr__(self):
        return "<{} status: {}>".format(
            self.__class__.__name__, self.status_int)

    def to_dict(self):
        """Convert this to a dictionary, usually for JSON output."""
        return dict(
            messages=[m.to_dict() for m in self.messages],
            toasts=[m.to_dict() for m in self.toasts],
            debug=self.debug,
            redirect=self.redirect)

    def add_message(self, title, kind=None, plain=None, html=None):
        """Add to the grave messages to be displayed to the user on the UI."""
        self.messages.append(UIMessage(
            title, kind=kind or self.DEFAULT_KIND, plain=plain, html=html))

    def add_toast(self, title, kind=None, plain=None, html=None):
        """Add to the quick messages to be displayed to the user on the UI."""
        self.toasts.append(UIMessage(
            title, kind=kind or self.DEFAULT_KIND, plain=plain, html=html))


class Rezulto(Returnable):
    """Response object returned from a successful operation.

    Unsuccessful operations raise exceptions instead.
    """

    DEFAULT_KIND = 'success'

    def __init__(self):
        """Constructor."""
        super().__init__()
        self.payload = {}
        self.status_int = 200  # HTTP response code indicating success

    def to_dict(self):
        """Convert instance to a dictionary, usually for JSON output."""
        return self.__dict__.copy()


class MalbonaRezulto(Returnable, Exception):
    """Base class for exceptions raised by actions."""

    DEFAULT_KIND = 'danger'

    def __init__(self, status_int: int=400, title: str=None, plain: str=None,
                 html: str=None, kind: str='danger'):
        """Constructor."""
        Returnable.__init__(self)
        self.status_int = status_int
        if title or plain or html:
            self.add_message(
                title=title, kind=kind, plain=plain, html=html)
