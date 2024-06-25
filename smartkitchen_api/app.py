from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from smartkitchen_api.api.router import api_router

app = FastAPI(
    title='smart kitchen',
    version='0.1.0',
    description='APP perfeito para salva as suas receitas favoritas.',
)

app.include_router(api_router, prefix='/api')

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', response_class=HTMLResponse)
async def read_root():
    html_content = """
    <html>
        <head>
            <title>SmartKitchen</title>
        </head>
        <body>
            <h1>SmartKitchen</h1>
            <p>Welcome to SmartKitchen!</p>
            <p>
              <a href="
                https://crispy-journey-596qqp77rgq34gq5-8000.app.github.dev/docs
                ">Click here
              </a> for more information about the documentation.
            </p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', reload=True, log_level='info')
