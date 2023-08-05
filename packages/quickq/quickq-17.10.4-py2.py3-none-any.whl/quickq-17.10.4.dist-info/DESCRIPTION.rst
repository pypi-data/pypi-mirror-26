# Django Quick Queue

Django Quick Queue is a fast and simple way to use async tasks in Django. This package has a limited use case. If you are looking for a more complex async task systems you should try Django Q, Celery, or Huey. Quick Queue is meant to give you the simplest method to get started executing small asynchronous tasks.

# Installation

### 1. Install Package

`pip install quickq`

### 2. Add Base URL to settings.py

```python
QQ_BASE_URL = 'https://mysite.example.com'
```

### 3. Setup the view in your urls.py

```python
from quickq import taskinator

urlpatterns = [
  url(r'^taskinator/(\S+)$', taskinator, name="taskinator"),
  ...
]
```

### 4. Add the Task decorator to any function

```python
from quickq import Task

@Task()
def send_approved (name, slug, email):
    send_mail(
      'Yay E-mail!',
      message,
      settings.DEFAULT_FROM_EMAIL,
      [email],
      fail_silently=False,
    )

# With a custom Timeout
@Task(timeout=120)
def another_task ():
  do_stuff()
```

### 5. Execute your task as normal

```python
send_email('Narf', 'narf-me', 'narf@aol.com')
```

## How it Works

1. Your task is called
    1. A PyJWT is generated.
    2. The taskinator URL is called asynchronously.
2. Taskinator view executed
    1. Decodes the JWT.
    2. Excutes the original task function outside of the original request.

## Limitations

- Function arguments are converted to JSON so they must be JSON compatible.
- Request time may be limited. If your webserver has a limitation on request time then that will also affect how long your tasks can execute since they are simply web requests. The request is also limited by the `QQ_REQUEST_TIMEOUT` setting.

## Additional Settings

```
QQ_TOKEN_EXPIRATION: Default 60
QQ_TOKEN_ALGORITHMS: Default ['HS256']
QQ_URL_NAME: Default 'taskinator'
QQ_REQUEST_TIMEOUT: Default 60
```

## Scaling

While Quick Queue is limited it still could scaled in with a few tricks.

- Run a separate web server just for Queue tasks. This would allow you scale your task queue differently and change your request timeout values.
- additional?

## Future Goals

- add task retries
- multiple queue URLs


