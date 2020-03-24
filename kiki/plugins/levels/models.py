"""
Levels models.
"""

import orm
from kiki.utils.db import database, metadata


class User(orm.Model):
    """
    Model to represent Discord Users and their server experience.
    """

    __tablename__ = "users"
    __database__ = database
    __metadata__ = metadata

    # String ID corresponding to the Discord User ID
    id = orm.String(primary_key=True, unique=True, max_length=32)

    # Experience value.
    experience = orm.Integer()

    @property
    def level(self):
        """
        Calculate the users level based on their experience value.
        """

        # Set boilerplate variables.
        xp = self.experience
        level = 0

        # Drain the XP and increment each level as it passes.
        while True:
            needed = 5 * (level ** 2) + 50 * level + 100
            if xp - needed >= 0:
                xp -= needed
                level += 1
            else:
                break

        # Return that value.
        return level
