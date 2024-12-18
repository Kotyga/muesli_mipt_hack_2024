import httpx
from datetime import datetime as dt
from uuid import uuid4
import aiofiles as aiof
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = {"access_token": os.getenv('ACCESS_TOKEN'),
         "expires_at": int(os.getenv('EXPIRES_AT'))}


async def get_access_token() -> str:
    if (
        not TOKEN["access_token"]
        or dt.fromtimestamp(TOKEN["expires_at"] / 1000) < dt.now()
    ):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid4()),
            "Authorization": f"Basic {os.getenv('AUTH_KEY')}",
        }
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.post(
                url=os.getenv('SBER_OAUTH_URL'),
                headers=headers,
                data={"scope": os.getenv('SBER_API_SCOPE')},
            )
            if resp.status_code != 200:
                print(resp.content)
                return ""

        token = resp.json()
        TOKEN["access_token"] = token["access_token"]
        TOKEN["expires_at"] = token["expires_at"]
    return TOKEN["access_token"]


async def text_to_speech(text: str) -> str:
    acc_token: str = await get_access_token()
    if not acc_token:
        print(f"Authentication error")
        return ""
    headers = {
        "Authorization": f"Bearer {acc_token}",
        "Content-Type": "application/text",
    }
    params = {
        "format": os.getenv('SPEECH_FILE_FORMAT'),
        "voice": os.getenv('VOICE_TYPE'),
    }
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.post(
            url=f"{os.getenv('SBER_SPEACH_URL')}/text:synthesize",
            headers=headers,
            params=params,
            content=text,
        )
        if resp.status_code != 200:
            print(resp.content)
            return ""
    file_name = f"speech_{uuid4()}.ogg"

    async with aiof.open(f"user_data/{file_name}", "wb") as f:
        await f.write(resp.content)
        await f.flush()
    return file_name


async def speech_to_text(speech_file: str, language: str) -> str:
    acc_token: str = await get_access_token()
    if not acc_token:
        print(f"Authentication error")
        return ""
    headers = {
        "Authorization": f"Bearer {acc_token}",
        "Content-Type": os.getenv('SPEECH_CONTENT_TYPE'),
    }
    params = {
        "language": language,
    }
    data = b""
    async with aiof.open(speech_file, "rb") as f:
        data = await f.read()
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.post(
            url=f"{os.getenv('SBER_SPEACH_URL')}/speech:recognize",
            headers=headers,
            params=params,
            content=data,
        )
        if resp.status_code != 200:
            print(resp.content)
            return ""
    speech_text: str = resp.json()["result"][0]
    return speech_text



