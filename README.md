[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/svaeva-redux/svaeva-redux/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/svaeva-redux/svaeva-redux/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/svaeva-redux/svaeva-redux/releases)
[![License](https://img.shields.io/github/license/svaeva-redux/svaeva-redux)](./LICENSE)

# Multi_API_Handler_Routes

## Introduction

- The Library is used to manage multiple APIs, as well as routing logic for directing requests to the appropriate endpoints.

| Problem | Solution |
| ------- | -------- |
| Allowing one endpoint to act as a gateway to multiple APIs | The Library is used to manage multiple APIs, as well as routing logic for directing requests to the appropriate endpoints. |

## Package Information

| Package | Version | License | Python |
| ------- | ------- | ------- | ------ |
| Multi_API_Handler_Routes | 0.1.0 | MIT | >=3.6 |

## Requirements

- Python >=3.6
- Poetry >=1.1.6

## Index

| Index |
| ----- |
| [Installation](#installation) |
| [Examples](#examples) |
| [Conclusion](#conclusion) |
| [License](#license) |

## Installation

```bash
poetry add git+https://github.com/Daise-Bell/Multi_API_Handler_Routes.git
```

# Examples

```python
from fastapi import FastAPI

from muilt_api_handler_routes.Routes.Configs  import ConfigsModel
from muilt_api_handler_routes.Routes.Skeleton import Skeleton

app = FastAPI()

app.include_router(Wallet(),    prefix="/v1/muiltapi")
app.include_router(ConfigModel(),  prefix="/v1/muiltapi")
app.include_router(Skeletons(),    prefix="/v1/muiltapi")
app.include_router(Virtual_Bound(),    prefix="/v1/muiltapi")
```


## Conclusion

- The Library is used to manage multiple APIs, as well as routing logic for directing requests to the appropriate endpoints.

## License
[![MIT](icons/license40.png)](https://choosealicense.com/licenses/mit/)

## Author
<a href="https://github.com/Vortex5Root">
    <div style="display: flex; align-items: center; height: 100px; width: 300px;">
        <img src=https://avatars.githubusercontent.com/u/102427260?v=4 width=50 style="border-radius: 50%;">
        <a href="https://github.com/Vortex5Root">Vortex5Root {Full-Stack Engineer}</a>
    </div>
</a>