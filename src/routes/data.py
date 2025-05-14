from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, settings
from controllers import DataController, ProjectController
import os
import aiofiles
import logging


logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, 
                     app_settings: settings = Depends(get_settings)):
    
    "VALIDATE FILE PROPERTIES"
    data_controller = DataController()
    is_valid = data_controller.validate_file(file=file)
    if not is_valid[0]:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": is_valid[1]},
        )
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_name = data_controller.generate_unique_file_name(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Error writing file: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"Error writing file: {str(e)}"},
        )
    return JSONResponse(
        content = {"message": "File uploaded successfully",
        "file_id": file_name}
    )
