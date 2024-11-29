#from typing import Union
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile, File, Form
from fastapi import HTTPException
from src.lib.Face_Streaming import Face
from src.database.mysql import mycursor
from typing import List
import json

app = FastAPI()
stream = Face()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/public", StaticFiles(directory="public"), name="public")


@app.get("/")
def read_root():
    return {"Hello": "World"} 

@app.get("/api/v1/images")
def get_img():
    mycursor.execute("SELECT id, name, note, image_name FROM CPE422.users")
    result = mycursor.fetchall()
    
    if result is None:
        raise HTTPException(status_code=500, detail="Database query failed.")
    elif not result:
        raise HTTPException(status_code=404, detail="No users found.")
    response_data = []
    for data in result:
        if "image_name" in data and data["image_name"]:
            data["image_name"] = json.loads(data["image_name"])  # Parse image_name
        response_data.append({
            "key": data["id"],
            "name": data["name"],
            "note": data["note"],
            "image_name": data["image_name"]
        })
    return JSONResponse(status_code=200, content=response_data)

@app.post("/api/v1/upload")
async def upload_images(name: str = Form(...),note: str = Form(...), images: List[UploadFile] = File(...)):
     await stream.saveImage(name, images)
     result = await stream.readImg_encoding(f"public/{name}",name, note)
     if result:
        raise HTTPException(status_code=201, detail={"message": "Images uploaded successfully"})
     else:
        raise HTTPException(status_code=400, detail={"message": "Images upload error"})

@app.get("/api/v1/video")
def video_feed():
    stream.get_data_encoding_db()
    return StreamingResponse(stream.open(), media_type="multipart/x-mixed-replace; boundary=frame")

