"""Repositories are persistence strategies.

The repository pattern describes a storage component that can be easily
swapped through dependency injection.

The purposes of a repository are:

1. To give a name to each query so the code becomes easier to read
2. To isolate data access code
3. Such that you can easily write unit tests (not integration tests) for the
   action / business layer. Because it is much, much easier to fake a
   repository than it is to fake SQLAlchemy and other ORMs.

Tests become easier to write because a repository is
dependency-injected into the action/service layer.

Extracting a repository from existing code does reveal repeated queries -- and
repetition is the root of all evil in software creation.

Notably absent from the above list of purposes is the dream of
easily swapping data access technology. The repository pattern does not
make the dream come true because persistence frameworks have their own
ideas about the models, too. For instance:

- ZODB is for when you traverse a lot; SQLALchemy is for when you search
  and query a lot. Usually it doesn't make sense to keep swapping
  between these two because they have different use cases.
- In SQLALchemy you model many-to-many relationships through an association
  table; in ZODB you usually do this in a very different way. Repositories
  for each tech would need to capture this.
- ZODB is very Pythonic, you include a lot of code in constructors.
  But SQLAlchemy is best used without constructors in the model classes.

In the end these differences make it very hard to develop software
that is so abstract that it deals with both techs well.

If in addition to different repositories you need to develop different models
for each tech, then there is no real code reuse, is there?

So the main purpose of a repository is to isolate IO so you can write
real unit tests for the pure part of the code.

I also recommend against building generic repositories. See
http://ben-morris.com/why-the-generic-repository-is-just-a-lazy-anti-pattern
"""

from bag.settings import resolve


def compose_class(name, mixins):
    """Return a class called ``name``, made of the bases ``mixins``."""
    bases = (resolve(mixin) if isinstance(mixin, str) else mixin
             for mixin in mixins)
    return type(name, tuple(bases), {})


class RepositoryAssembler:
    """Lets application modules contribute mixins to the repository class."""

    def __init__(self, mixins=None):
        self.repository_mixins = list(mixins) if mixins else []
        self._Repository = None

    def add_repository_mixin(self, mixin):
        """Store another mixin class that will form the final repository."""
        assert isinstance(mixin, (str, type))
        self.repository_mixins.append(mixin)
        self._Repository = None

    @property
    def Repository(self):
        """Return the Repository class.

        On 1st access, assembles the Repository class from registered mixins.
        """
        if not self._Repository:
            self._Repository = compose_class(
                name='Repository', mixins=self.repository_mixins)
        return self._Repository
