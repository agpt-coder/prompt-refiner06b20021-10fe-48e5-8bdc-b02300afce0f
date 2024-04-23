import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.get_user_info_service
import project.login_service
import project.logout_service
import project.refine_prompt_service
import project.update_profile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="prompt refiner",
    lifespan=lifespan,
    description="To accomplish the task of creating a single API endpoint that takes in a string LLM prompt and returns a refined version improved by GPT4, several steps and pieces of information are critical based on our discussion and research. First, integration of the OpenAI Python package with FastAPI is essential. The process begins with installing the OpenAI package via pip. After installation, it's necessary to import OpenAI into the FastAPI application to facilitate communication with GPT-4. The core functionality involves creating an endpoint, for example, `/refine-prompt`, within the FastAPI app, which accepts a LLM prompt from the user as the request body. This endpoint will process the input by sending it to the OpenAI API, specifying GPT-4 as the model, along with the system's instruction: 'You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt.' Once GPT-4 processes and refines the prompt based on the given instruction, the refined prompt is then returned to the user as the response. The tech stack for this implementation includes Python as the programming language, FastAPI as the API framework, PostgreSQL for any required database functionality, and Prisma as the ORM. This detailed approach ensures a robust and efficient system for refining user prompts through GPT-4, leveraging FastAPI's asynchronous handling and OpenAI's powerful language model.",
)


@app.get("/user/info", response_model=project.get_user_info_service.UserInfoResponse)
async def api_get_get_user_info() -> project.get_user_info_service.UserInfoResponse | Response:
    """
    Retrieves user profile information.
    """
    try:
        res = await project.get_user_info_service.get_user_info()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/refine-prompt", response_model=project.refine_prompt_service.RefinePromptResponse
)
async def api_post_refine_prompt(
    prompt: str,
) -> project.refine_prompt_service.RefinePromptResponse | Response:
    """
    Accepts a language model prompt from the user and returns a refined version.
    """
    try:
        res = await project.refine_prompt_service.refine_prompt(prompt)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/logout", response_model=project.logout_service.LogoutResponse)
async def api_post_logout(
    Authorization: str,
) -> project.logout_service.LogoutResponse | Response:
    """
    Invalidates the user's JWT token to safely end a session.
    """
    try:
        res = await project.logout_service.logout(Authorization)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile",
    response_model=project.update_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_profile(
    name: Optional[str],
    email: Optional[str],
    bio: Optional[str],
    location: Optional[str],
) -> project.update_profile_service.UpdateUserProfileResponse | Response:
    """
    Allows users to update their profile information.
    """
    try:
        res = await project.update_profile_service.update_profile(
            name, email, bio, location
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.login_service.LoginResponse)
async def api_post_login(
    username: str, password: str
) -> project.login_service.LoginResponse | Response:
    """
    Authenticates users and returns a JWT token.
    """
    try:
        res = await project.login_service.login(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
