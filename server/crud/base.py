from sqlalchemy.ext.asyncio import AsyncSession


class CRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
