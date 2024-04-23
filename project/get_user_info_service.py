import prisma
import prisma.models
from pydantic import BaseModel


class UserInfoResponse(BaseModel):
    """
    Provides detailed user information, excluding sensitive data like password for security reasons.
    """

    id: str
    email: str
    createdAt: str
    updatedAt: str
    role: str


async def get_user_info() -> UserInfoResponse:
    """
    Retrieves user profile information.

    This function fetches the current user's information from the database, excluding any sensitive data such as the password.
    It returns an object of type UserInfoResponse populated with the user's details.

    Args:
        None

    Returns:
        UserInfoResponse: An object containing detailed information about the current user, excluding the password.

    Example:
        > await get_user_info()
        UserInfoResponse(id="...", email="user@example.com", createdAt="...", updatedAt="...", role="USER")
    """
    current_user_id = "current_user_unique_id"
    user_info = await prisma.models.User.prisma().find_unique(
        where={"id": current_user_id}
    )
    if not user_info:
        raise Exception("User not found")
    return UserInfoResponse(
        id=user_info.id,
        email=user_info.email,
        createdAt=user_info.createdAt.isoformat(),
        updatedAt=user_info.updatedAt.isoformat(),
        role=user_info.role.name,
    )
