import openai
from pydantic import BaseModel


class RefinePromptResponse(BaseModel):
    """
    Returns the original and refined prompt alongside any pertinent metadata.
    """

    original_prompt: str
    refined_prompt: str
    refinement_status: str


async def refine_prompt(prompt: str) -> RefinePromptResponse:
    """
    Accepts a language model prompt from the user and returns a refined version. Utilizes the OpenAI API to process
    and refine the input prompt via GPT-4 with specific instructions for improvement.

    Args:
        prompt (str): The raw language model prompt input by the user for refinement.

    Returns:
        RefinePromptResponse: Returns the original and refined prompt alongside any pertinent metadata, including
        the success or failure status of the refinement process.
    """
    openai.api_key = "your-openai-api-key"
    try:
        response = openai.Completion.create(
            model="text-davinci-004",
            prompt=f"You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt: {prompt}",
            max_tokens=150,
        )  # TODO(autogpt): "Completion" is not a known attribute of module "openai". reportAttributeAccessIssue
        refined_prompt = (
            response["choices"][0]["text"].strip() if response["choices"] else ""
        )
        return RefinePromptResponse(
            original_prompt=prompt,
            refined_prompt=refined_prompt,
            refinement_status="COMPLETED" if refined_prompt else "FAILED",
        )
    except Exception as e:
        return RefinePromptResponse(
            original_prompt=prompt,
            refined_prompt="",
            refinement_status=f"FAILED due to an internal error: {e}",
        )
