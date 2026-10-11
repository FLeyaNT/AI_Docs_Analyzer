import logging

import uvicorn

from fastapi.responses import HTMLResponse

from app.create_app import create_app
from app.core.config import settings
from app.api.api import router_v1


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format
)

app = create_app()

app.include_router(
    router=router_v1,
    prefix='/api',
)


@app.get("/")
async def files():
    content = """
<body>
<form action="api/v1/upload/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


if __name__ == '__main__':
    uvicorn.run(
        app='app.main:app',
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
        reload_dirs=['app']
    )
