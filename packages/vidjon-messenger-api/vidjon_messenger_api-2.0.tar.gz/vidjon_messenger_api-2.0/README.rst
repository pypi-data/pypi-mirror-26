#vidjon_messenger_api
A simple messenger API for sending and receiving messages with authorization.
The solution is available as a PyPI package.

##Local Deployment
Create a virtual environment for the package to be able to run using package virtualenv.
Download the messenger API using pip and run the package. The messenger API is deployed locally
on http://localhost:5000

###Unix
```
$ pip install virtualenv
$ virtualenv venv
$ cd venv
$ source bin/activate
$ pip install vidjon_messenger_api
$ vidjon_messenger_api
```
###Windows
```
> pip install virtualenv
> virtualenv venv
> cd venv
> Scripts\activate
> pip install vidjon_messenger_api
> vidjon_messenger_api
```
##Using the API

###Register User
```
curl -X POST \
  http://localhost:5000/register \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
	"username": "vidjon",
	"password": "asdf"
}'
```
```
{
    "message": "User created successfully."
}
```
###Get authorization key
```
curl -X POST \
  http://localhost:5000/auth \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
	"username": "vidjon",
	"password": "asdf"
}'
```
```
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDg0NDUyNDMsImlhdCI6MTUwODQ0NDk0MywibmJmIjoxNTA4NDQ0OTQzLCJpZGVudGl0eSI6M30.BBXkvGoxhx6VYWSuaIDW_745C8WDserpczVoNX7X15E"
}
```
###Get Messages
```
curl -X GET \
  http://localhost:5000/message \
  -H 'authorization: JWT <ACCESS-TOKEN> \
  -H 'cache-control: no-cache'
```
###Get Messages by start and stop
```
curl -X GET \
  'http://localhost:5000/message?start=1&stop=5' \
  -H 'authorization: JWT <ACCESS-TOKEN> \
  -H 'cache-control: no-cache' \
  -H 'postman-token: eec4a390-5aef-685c-840f-a72932e9ee26'
```
###Send Message
```
curl -X POST \
  http://localhost:5000/message \
  -H 'authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDg0NDYyMDUsImlhdCI6MTUwODQ0NTkwNSwibmJmIjoxNTA4NDQ1OTA1LCJpZGVudGl0eSI6M30.wS_pcQgoW4iRJvzvQAnx_Y_plJKVk4LGO32W2oU70ME' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
	"to_user": "vidjon",
	"content": "Hello bob1!"
}'
```
###Delete Messages by Id
```
curl -X DELETE \
  http://localhost:5000/message \
  -H 'authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDg0NDYyMDUsImlhdCI6MTUwODQ0NTkwNSwibmJmIjoxNTA4NDQ1OTA1LCJpZGVudGl0eSI6M30.wS_pcQgoW4iRJvzvQAnx_Y_plJKVk4LGO32W2oU70ME' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
	"ids": [1,2]
}'
```