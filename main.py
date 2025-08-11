from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/test")
async def test(request: Request):
    form = await request.form()
    return {"form_data": dict(form)}

@app.get("/")
async def root():
    return {"message": "Server is running"}
