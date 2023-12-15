from typing import Optional, Dict, List

from app.firebase import db
from app.models import FaceSwapPackage, FaceSwapPackageName


async def get_face_swap_package(face_swap_package_id: str) -> Optional[FaceSwapPackage]:
    face_swap_package_ref = db.collection("face_swap_packages").document(str(face_swap_package_id))
    face_swap_package = await face_swap_package_ref.get()

    if face_swap_package.exists:
        return FaceSwapPackage(**face_swap_package.to_dict())


async def get_face_swap_package_by_user_id_and_name(user_id: str,
                                                    name: str) -> Optional[FaceSwapPackage]:
    face_swap_package_stream = db.collection("face_swap_packages") \
        .where("user_id", "==", user_id) \
        .where("name", "==", name) \
        .limit(1) \
        .stream()

    async for doc in face_swap_package_stream:
        return FaceSwapPackage(**doc.to_dict())


async def create_face_swap_package_object(user_id: str,
                                          name: str,
                                          used_images: List[str]) -> FaceSwapPackage:
    face_swap_package_ref = db.collection('face_swap_packages').document()
    return FaceSwapPackage(
        id=face_swap_package_ref.id,
        user_id=user_id,
        name=name,
        used_images=used_images
    )


async def write_face_swap_package(user_id: str,
                                  name: str,
                                  used_images: List[str]) -> FaceSwapPackage:
    face_swap_package = await create_face_swap_package_object(user_id, name, used_images)
    await db.collection('face_swap_packages').document(face_swap_package.id).set(face_swap_package.to_dict())

    return face_swap_package


async def update_face_swap_package(package_id: str, data: Dict):
    face_swap_package_ref = db.collection('face_swap_packages').document(package_id)
    await face_swap_package_ref.update(data)
