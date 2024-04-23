from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    This model provides the output for the update user profile API endpoint, confirming the successful update of user information.
    """

    success: bool
    message: str
    updated_fields: List[str]


async def update_profile(
    name: Optional[str],
    email: Optional[str],
    bio: Optional[str],
    location: Optional[str],
) -> UpdateUserProfileResponse:
    """
    Allows users to update their profile information.

    This function updates the user's profile information such as name, email, bio, and location in the database.
    It ensures that only valid changes are applied and returns the fields that were successfully updated.

    Args:
        name (Optional[str]): The user's updated full name.
        email (Optional[str]): The user's updated email address.
        bio (Optional[str]): A short user biography or personal statement.
        location (Optional[str]): The user's updated location information.

    Returns:
        UpdateUserProfileResponse: This model provides the output for the update user profile API endpoint,
        confirming the successful update of user information including which fields were updated.

    Example:
        response = await update_profile(name="John Doe", email=None, bio="An avid reader and writer.", location="New York")
        > UpdateUserProfileResponse(success=True, message="Profile updated successfully", updated_fields=["name", "bio", "location"])
    """
    updated_fields = []
    user_id = "current_user_id"
    try:
        user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
        if not user:
            return UpdateUserProfileResponse(
                success=False, message="User not found.", updated_fields=[]
            )
        update_data = {}
        if name:
            update_data["name"] = name
            updated_fields.append("name")
        if email:
            update_data["email"] = email
            updated_fields.append("email")
        if bio:
            update_data["bio"] = bio
            updated_fields.append("bio")
        if location:
            update_data["location"] = location
            updated_fields.append("location")
        if update_data:
            await prisma.models.User.prisma().update(
                where={"id": user_id}, data=update_data
            )
            return UpdateUserProfileResponse(
                success=True,
                message="Profile updated successfully.",
                updated_fields=updated_fields,
            )
        else:
            return UpdateUserProfileResponse(
                success=False,
                message="No valid fields provided for update.",
                updated_fields=[],
            )
    except Exception as e:
        return UpdateUserProfileResponse(
            success=False,
            message=f"Failed to update user profile: {str(e)}",
            updated_fields=[],
        )
