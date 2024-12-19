from fastapi import FastAPI, UploadFile, File, HTTPException
from pymongo import MongoClient
from bson import ObjectId
import oci
from models.student import Student
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# MongoDB configuration
mongo_uri = os.getenv("MONGODB_CONNECTION_STRING")
client = MongoClient(mongo_uri)
db = client.school_db

# Oracle Cloud Infrastructure (OCI) Object Storage configuration
config = oci.config.from_file("config", "DEFAULT")
object_storage = oci.object_storage.ObjectStorageClient(config)
namespace = object_storage.get_namespace().data

# Variables for Object Storage
bucket_name = os.getenv("ORACLE_BUCKET_NAME")
region = config["region"]

"""
Test API via Swagger using /docs
"""

@app.post("/students/")
async def create_student(name: str, grade: float, photo: UploadFile = File(...)):
    """
    Create a new student with their details and upload the photo to Oracle Object Storage.

    Args:
        name (str): Name of the student (MongoDB)
        grade (float): The grade of the student (MongoDB)
        photo (UploadFile): The photo (Oracle Bucket)
    """
    try:
        # Read the photo content
        photo_content = await photo.read()

        # Upload the photo to Oracle Cloud Object Storage
        object_name = f"photos/{name}_{photo.filename}"
        object_storage.put_object(
            namespace_name=namespace,
            bucket_name=bucket_name,
            object_name=object_name,
            put_object_body=photo_content
        )

        # Generate the photo URL
        photo_url = f"https://objectstorage.{region}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o/{object_name}"

        student = Student(name=name, grade=grade, photo_url=photo_url)

        result = db.students.insert_one(student.model_dump())

        return {**student.model_dump(), "_id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating student: {str(e)}")

@app.get("/students/{student_id}")
async def get_student(student_id: str):
    """
    Retrieve a student by their ID from MongoDB.

    MongoDB (_id, name, grade, photo_url)
    """
    try:
        student = db.students.find_one({"_id": ObjectId(student_id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return {**student, "_id": str(student["_id"])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving student: {str(e)}")

@app.get("/students/")
async def list_students():
    """
    List all students in the database.

    Returns:
        List of student objects
    """
    try:
        students = list(db.students.find())
        return [{**student, "_id": str(student["_id"])} for student in students]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing students: {str(e)}")

@app.put("/students/{student_id}")
async def update_student(student_id: str, student_data: Student):
    """
    Update a student's details by their ID in MongoDB.
    """
    try:
        result = db.students.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": student_data.model_dump()}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return student_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating student: {str(e)}")

@app.delete("/students/{student_id}")
async def delete_student(student_id: str):
    """
    Delete a student by their ID from MongoDB.
    """
    try:
        result = db.students.delete_one({"_id": ObjectId(student_id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"message": "Student deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting student: {str(e)}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
