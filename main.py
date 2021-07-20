from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
import httpx
from starlette.config import Config

from typing import List
from pydantic import BaseModel

# Load environment variables
config = Config('.env')

app = FastAPI()



# Define the auth scheme and access token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Validate the token
def validate(token: str = Depends(oauth2_scheme)):
    # TODO: Add token validation logic
    return True


# Data model
class Item(BaseModel):
    id: int
    name: str


# Protected, get items route
@app.get('/items', response_model=List[Item])
def read_items(valid: bool = Depends(validate)):
    return [
        Item.parse_obj({'id': 1, 'name': 'red ball'}),
        Item.parse_obj({'id': 2, 'name': 'blue square'}),
        Item.parse_obj({'id': 3, 'name': 'purple ellipse'}),
    ]

# Call the Okta API to get an access token
def retrieve_token(authorization, issuer, scope='items'):
    headers = {
        'accept': 'application/json',
        'authorization': authorization,
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': scope,
    }
    url = issuer + '/v1/token'

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail=response.text)


# Get auth token endpoint
@app.post('/token')
def login(request: Request):
    return retrieve_token(
        request.headers['authorization'],
        config('OKTA_ISSUER'),
        'items'
    )