from fastapi import FastAPI, Response, HTTPException, status, Header
import requests
import json
import io
from classes import *
import os

app = FastAPI()
headers = {'Content-Type': 'application/json'}

addr = os.environ.get('IP_ADDR', 'localhost')


@app.get('/search')
async def search(query: str = None, authorization: str = Header(None)):
    if query is not None and authorization is not None:
        data = {
            'refreshToken': authorization.split(' ')[1]     
        }
        data_headers = {
            'Authorization': authorization,
            'Content-Type': 'application/json'
        }
        user_respoonse = requests.post(f'http://{addr}:8079/verifytoken', headers=data_headers, data=json.dumps(data))
        if user_respoonse.status_code == 200:
            response = requests.get(f'http://{addr}:8080/search?q={query}')
            if response.status_code == 200:
                body = json.loads(response.content.decode('utf-8'))
                return body
            else:
                raise HTTPException(
                    status_code=500,
                    detail='Internal Server Error',
                )
        else:
            raise HTTPException(
                    status_code=401,
                    detail='User is not allowed to access this methode',
                )
    else:
        raise HTTPException(
                    status_code=400,
                    detail='Invalid request',
                )
    

@app.get('/get_history')
async def get_history(authorization: str = Header(None)):
    if authorization is not None:
        data_header = {
            'Authorization': authorization,
            'Content-Type': 'application/json'
        }
        response = requests.get(f'http://{addr}:8079/transaction/get_history', headers=data_header)
        if response.status_code == 200:
            body = json.loads(response.content.decode('utf-8'))
            return body
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            )
    else:
        raise HTTPException(
                    status_code=400,
                    detail='Invalid request',
                )
    
@app.get('/graph/popular')
async def get_popular(authorization: str = Header(None)):
    if authorization is not None:
        data_header = {
            'Authorization': authorization,
            'Content-Type': 'application/json'
        }
        response = requests.get(f'http://{addr}:8079/transaction/get_popular_transactions', headers=data_header)
        if response.status_code == 200:
            body = json.loads(response.content.decode('utf-8'))
            return body
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            )
    else:
        raise HTTPException(
                    status_code=400,
                    detail='Invalid request',
        )
    
@app.get('/graph/price')
async def get_price(authorization: str = Header(None)):
    if authorization is not None:
        data_header = {
            'Authorization': authorization,
            'Content-Type': 'application/json'
        }
        response = requests.get(f'http://{addr}:8079/transaction/get_transactions_price', headers=data_header)
        if response.status_code == 200:
            body = json.loads(response.content.decode('utf-8'))
            return body
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            )
    else:
        raise HTTPException(
                    status_code=400,
                    detail='Invalid request',
        )

@app.post('/save_transaction')
async def save_transaction(transaction: Transaction, authorization: str = Header(None)):
    if transaction is not None and authorization is not None:
        data_headers = {
            'Authorization': authorization,
            'Content-Type': 'application/json'
        }
        data = {
            "datasetName": transaction.database_name
        }
        response = requests.post(f'http://{addr}:8079/transaction/save_transaction', headers=data_headers, data=json.dumps(data))
        if response.status_code == 201:
            return {"message": "Transaction saved successfully!"}
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            )
    else:
        raise HTTPException(
                    status_code=400,
                    detail='Invalid request',
                )
    

@app.get('/display_snippet')
async def display_snippet(database_name: str = None, database_table: str = None, authorization: str = Header(None)):
    if database_name is not None and database_table is not None and authorization is not None:
        data = {
            'refreshToken': authorization.split(' ')[1]     
        }
        data_headers = {
            'Authorization': authorization,
            'Content-Type': 'application/json'
        }
        user_respoonse = requests.post(f'http://{addr}:8079/verifytoken', headers=data_headers, data=json.dumps(data))
        if user_respoonse.status_code == 200:
            response = requests.get(f'http://{addr}:8080/get_snippet?databaseName={database_name}&databaseTable={database_table}')
            if response.status_code == 200:
                body = json.loads(response.content.decode('utf-8'))
                return body
            else:
                raise HTTPException(
                    status_code=500,
                    detail='Internal Server Error',
                )
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid request',
        )
    

@app.get('/get_full_dataset')
async def get_full_dataset(database_name: str = None, database_table: str = None, data_format: str = None, authorization: str = Header(None)):
    if database_name is not None and database_table is not None and data_format is not None and authorization is not None:
        data = {
            'refreshToken': authorization.split(' ')[1]     
        }
        data_headers = {
            'Authorization': authorization,
            'Content-Type': 'application/json'
        }
        user_respoonse = requests.post(f'http://{addr}:8079/verifytoken', headers=data_headers, data=json.dumps(data))
        if user_respoonse.status_code == 200:
            response = requests.get(f'http://{addr}:8080/get_dataset?databaseName={database_name}&databaseTable={database_table}&format={data_format}')
            if response.status_code == 200:
                body = response.content.decode("utf-8")
                if data_format == 'json' or data_format == 'json-ld':
                    body = json.dumps(body)
                    file = io.StringIO(body)
                else:
                    file = io.StringIO(body)

                response = Response(content=file.getvalue())
                response.headers["Content-Disposition"] = f"attachment; filename={database_table}.{data_format}"
                response.headers["Content-Type"] = "application/json"
                return response
            else:
                raise HTTPException(
                    status_code=500,
                    detail='Internal Server Error',
                )
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            )  
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid request',
        )
    
@app.post('/signin')
async def signin(signins: Signin):
    if signins.username is not None and signins.password is not None:
        data = {
            "username": signins.username,
            "password": signins.password
        }
        user_response = requests.post(f'http://{addr}:8079/signin', headers=headers, data=json.dumps(data))
        if user_response.status_code == 200:
            body = json.loads(user_response.content.decode("utf-8"))
            return {"message": "Logged in successfully!", "user_data": body}
        else:
            raise HTTPException(
                status_code=500,
                detail=user_response.content.decode("utf-8"),
            )
    else:
        raise HTTPException(
                status_code=400,
                detail='Invalid request',
            )

@app.post('/signup')
async def signup(signups: Signup):
    if signups.username is not None and signups.password is not None and signups.email is not None:
        data = {
            "username": signups.username,
            "email": signups.email,
            "password": signups.password
        }
        user_response = requests.post(f'http://{addr}:8079/signup', headers=headers, data=json.dumps(data))
        if user_response.status_code == 200:
            email_response = requests.get(f'http://{addr}:8079/sendEmail/{signups.email}')
            if email_response.status_code == 200:
                return {"message": "Account created successfully! (Check your email for to verify your account)"}
            else:
                raise HTTPException(
                    status_code=500,
                    detail=email_response.content.decode("utf-8"),
                )
        else:
            raise HTTPException(
                status_code=500,
                detail=user_response.content.decode("utf-8"),
            )
    else:
        raise HTTPException(
                status_code=400,
                detail='Invalid request',
            )
    

@app.post('/validate_email')
async def validate_email(validate: Validate):
        if validate.email is not None and validate.code is not None:
            data = {
                "code": validate.code
            }
            user_response = requests.post(f'http://{addr}:8079/validate_code/{validate.email}', headers=headers, data=json.dumps(data))
            if user_response.status_code == 200:
                return {"message": "Account validation successful!"}
            else:
                raise HTTPException(
                    status_code=500,
                    detail=user_response.content.decode("utf-8"),
                )
        else:
            raise HTTPException(
                status_code=400,
                detail='Invalid request',
            )


@app.get('/signout')
async def signout(authorization: str = Header(None)):
        data_headers = {
            'Authorization': authorization,
            'Content-Type': 'application/json'
        }
        user_response = requests.get(f'http://{addr}:8079/signout', headers=data_headers)
        if user_response.status_code == 200:
            return {"message": "Logged out successfully!"}
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            ) 
        

@app.delete('/delete_account')
async def delete_account(delete: Delete, authorization: str = Header(None)):
    if authorization is not None and delete is not None:
        data_headers = {
                    'Authorization': authorization,
                    'Content-Type': 'application/json'
                }
        response = requests.delete(f'http://{addr}:8079/users/{delete.email}', headers=data_headers)
        if response.status_code == 200:
            return {"message": "Account deleted successfully!"}
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            ) 
    else:
        raise HTTPException(
                status_code=400,
                detail='Invalid request',
            )

@app.put('/update_password')
async def update_password(passwords: PasswordReset,  authorization: str = Header(None)):
    if passwords.current_password is not None and passwords.new_password is not None and authorization is not None:
        data_headers = {
            'Authorization': authorization,
            'Content-Type': 'application/json'
        }
        data = {
            "CurrentPassword": passwords.current_password,
            "newPassword": passwords.new_password
        }
        response = requests.put(f'http://{addr}:8079/users/password', headers=data_headers, data=json.dumps(data))
        if response.status_code == 200:
            return {"message": "Password updated successfully!"}
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid request',
        )


@app.get('/get_balance')
async def get_balance(authorization: str = Header(None)):
    if authorization is not None:
        data_headers = {
                    'Authorization': authorization,
                    'Content-Type': 'application/json'
                }
        balance_response = requests.get(f'http://{addr}:8079/check_balance', headers=data_headers)
        if balance_response.status_code == 200:
            return balance_response.json()
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid request',
        )


@app.post('/update_balance')
async def update_balance(balance: Balance, authorization: str = Header(None)):
    if authorization is not None and balance.balance is not None:
        data_headers = {
                    'Authorization': authorization,
                    'Content-Type': 'application/json'
                }
        data = {
            "balance": balance.balance
        }
        balance_response = requests.post(f'http://{addr}:8079/update_balance', headers=data_headers, data=json.dumps(data))
        if balance_response.status_code == 200:
            return balance_response.json()
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid request',
        )
    

@app.post('/refresh_token')
async def refresh_token(authorization: str = Header(None)):
    if authorization is not None:
        data_headers = {
                    'Authorization': authorization,
                    'Content-Type': 'application/json'
                }
        data = {
            "refreshToken": authorization.split(' ')[1]
        }
        response = requests.post(f'http://{addr}:8079/check_balance', headers=data_headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=401,
                detail='User is not allowed to access this methode!',
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid request',
        )