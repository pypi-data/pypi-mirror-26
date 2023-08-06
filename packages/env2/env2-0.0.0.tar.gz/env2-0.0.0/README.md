# Env2

os.environ on stereoids

env2 allows raising errors on missing environment variables without too much bolierplate code. This is very useful when developing microservices that depends on environment variables.

## How it works

With env2 you can replace this:

```python
import os

var = os.environ.get('key', None)
if not var:
    raise Exception(f'{key} not found in environment variables')
return var
```

With this:

```python
from env2 import env2

var = env2('key')
```

env2 will automatically raise on a missing key, to avoid that:

```python
from env2 import env2

var = env2('key', raise_error=False)
```

env2 allows to set default values as well:

```python
from env2 import env2

var = env2('key', default='key2')
```

## License

This software is under [WTFPL](http://www.wtfpl.net) license