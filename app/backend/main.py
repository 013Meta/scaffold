from fastapi import FastAPI, File, UploadFile
from deepgram import Deepgram
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")

# Ensure you're using the correct client initialization based on the SDK version
dg_client = Deepgram(deepgram_api_key)


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        return {"error": "File is not an audio type."}

    try:
        content = await file.read()
        # Assuming the SDK version you're using matches the documentation,
        # and the method for sending audio data directly (not from a file path or URL) is correctly used.
        # Note: The documentation provided does not explicitly cover this scenario,
        # so you might need to refer to the latest SDK documentation for the exact method.
        response = await asyncio.create_task(
            dg_client.transcribe({"content": content, "mime_type": file.content_type})
        )
        # Adjust the response parsing based on the actual structure of the response from Deepgram
        transcription = response["results"]["channels"][0]["alternatives"][0][
            "transcript"
        ]
        return {"transcription": transcription}
    except Exception as e:
        return {"error": str(e)}
