import prisma
import prisma.models
from pydantic import BaseModel


class LogoutResponse(BaseModel):
    """
    Confirms whether the user has been successfully logged out.
    """

    message: str


async def logout(Authorization: str) -> LogoutResponse:
    """
    Invalidates the user's JWT token to safely end a session.

    Args:
        Authorization (str): The bearer token used for authentication, supplied in the headers.

    Returns:
        LogoutResponse: Confirms whether the user has been successfully logged out.
    """
    token = Authorization.replace("Bearer ", "")
    deleted_token = await prisma.models.AccessToken.prisma().delete_many(
        where={"token": token}
    )
    if deleted_token > 0:
        return LogoutResponse(message="User logged out successfully.")
    else:
        return LogoutResponse(message="Invalid token or already logged out.")
