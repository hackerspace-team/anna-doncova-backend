from typing import List, Optional
from datetime import datetime, timezone

from google.cloud.firestore import Query

from AnnaDoncovaBot.firebase import db
from AnnaDoncovaBot.models.mini_course import MiniCourse


async def get_mini_course(mini_course_id: str) -> MiniCourse:
    mini_course_ref = db.collection("mini_courses").document(mini_course_id)
    mini_course = await mini_course_ref.get()

    if mini_course.exists:
        mini_course_dict = mini_course.to_dict()
        return MiniCourse(
            id=mini_course_dict.get('id', None),
            name=mini_course_dict.get('name', None),
            email=mini_course_dict.get('email', None),
            telegram=mini_course_dict.get('telegram', None),
            amount=mini_course_dict.get('amount', None),
            income_amount=mini_course_dict.get('income_amount', None),
            payment_id=mini_course_dict.get('payment_id', None),
            payment_method=mini_course_dict.get('payment_method', None),
            payment_status=mini_course_dict.get('payment_status', None),
            created_date=mini_course_dict.get('created_date', None),
            edited_date=mini_course_dict.get('edited_date', None),
        )


async def get_mini_course_by_payment_id(payment_id: str) -> MiniCourse:
    mini_course_stream = db.collection("mini_courses").where("payment_id", "==", payment_id).limit(1).stream()

    async for doc in mini_course_stream:
        mini_course_dict = doc.to_dict()
        return MiniCourse(
            id=mini_course_dict.get('id', None),
            name=mini_course_dict.get('name', None),
            email=mini_course_dict.get('email', None),
            telegram=mini_course_dict.get('telegram', None),
            amount=mini_course_dict.get('amount', None),
            income_amount=mini_course_dict.get('income_amount', None),
            payment_id=mini_course_dict.get('payment_id', None),
            payment_method=mini_course_dict.get('payment_method', None),
            payment_status=mini_course_dict.get('payment_status', None),
            created_date=mini_course_dict.get('created_date', None),
            edited_date=mini_course_dict.get('edited_date', None),
        )


async def get_mini_courses(start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None) -> List[MiniCourse]:
    mini_courses_query = db.collection("mini_courses")

    if start_date:
        mini_courses_query = mini_courses_query.where("created_date", ">=", start_date)
    if end_date:
        mini_courses_query = mini_courses_query.where("created_date", "<=", end_date)

    mini_courses = mini_courses_query.order_by("created_date", direction=Query.DESCENDING).stream()
    return [
        MiniCourse(
            id=mini_course.to_dict().get('id', None),
            name=mini_course.to_dict().get('name', None),
            email=mini_course.to_dict().get('email', None),
            telegram=mini_course.to_dict().get('telegram', None),
            amount=mini_course.to_dict().get('amount', None),
            income_amount=mini_course.to_dict().get('income_amount', None),
            payment_id=mini_course.to_dict().get('payment_id', None),
            payment_method=mini_course.to_dict().get('payment_method', None),
            payment_status=mini_course.to_dict().get('payment_status', None),
            created_date=mini_course.to_dict().get('created_date', None),
            edited_date=mini_course.to_dict().get('edited_date', None),
        ) async for mini_course in mini_courses
    ]


async def update_mini_course(mini_course_id: str, data: dict):
    mini_course_ref = db.collection('mini_courses').document(mini_course_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await mini_course_ref.update(data)

