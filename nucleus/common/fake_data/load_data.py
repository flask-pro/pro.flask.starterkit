import io
import os

from faker import Faker
from flask import current_app
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage

from nucleus.common.extensions import db
from nucleus.config import Config
from nucleus.controllers.articles import article_controller
from nucleus.controllers.directories import categories_controller
from nucleus.controllers.directories import Directory
from nucleus.controllers.feedbacks import feedback_controller
from nucleus.controllers.files import file_controller

ENV = Config.ENV
ICON_FILE_TO_CATEGORY_PATH = os.path.join(
    Config.BASE_DIR, "common", "fake_data", "category_icon.png"
)
IMAGE_FILE_PATH = os.path.join(Config.BASE_DIR, "common", "fake_data", "image.png")
AUTHOR_ICON_FILE_PATH = os.path.join(Config.BASE_DIR, "common", "fake_data", "author_icon.png")

fake = Faker(["ru_RU"])

articles = [
    {
        "title": "О НППХ",
        "content": "Что такое НППХ? НППХ — это ответ на существующие вызовы в системе подготовки "
        "спортивного резерва в хоккее. НППХ  разрабатывалась как практическая и "
        "идеологическая часть «Стратегии развития хоккея 2018-2020». НППХ является "
        "практическим инструментом решения вопросов проблематики, обозначенной в "
        "«Концепции подготовки спортивного резерва в Российской Федерации до 2025 "
        "года». НППХ — это сложный многоэтапный проект, в основе которого реализована "
        "идея повышения базового уровня технико-тактической подготовленности хоккеистов "
        "в процессе спортивной тренировки на начальном этапе, а также этапе спортивной "
        "специализации. НППХ полностью совместима с федеральными нормативными "
        "документами.",
        "global_name": "about_npph",
    }
]


def _load_categories(content_type: str, count: int = 5) -> list:
    try:
        for cat_count in range(count):
            with open(ICON_FILE_TO_CATEGORY_PATH, "rb") as icon:
                buffer = io.BytesIO(icon.read())
                icon_storage = FileStorage(
                    stream=buffer, filename="category_icon.png", content_type="image/png"
                )
                file = file_controller.create(icon_storage)
            categories_controller.create(
                {
                    "name": f"#{cat_count}# Категория {content_type}",
                    "content_type": content_type,
                    "icon_id": file.id,
                }
            )

    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.warning(f"Load init data | error load category | {repr(e)}")

    return Directory.get_directories()[content_type]["categories"]


def _load_articles(articles: list) -> None:
    for article in articles:
        try:
            with open(IMAGE_FILE_PATH, "rb") as image:
                buffer = io.BytesIO(image.read())
                image_storage = FileStorage(
                    stream=buffer, filename="image.png", content_type="image/png"
                )
                saved_image = file_controller.create(image_storage)
            article["main_picture_id"] = saved_image.id
            article_controller.create(article)
        except IntegrityError:
            db.session.rollback()
            current_app.logger.warning(f"Load init data | error load article | {article}")
            continue


def _load_feedbacks() -> None:
    categories = _load_categories("feedbacks", count=5)
    try:
        for count_feedback, category in enumerate(categories):
            new_feedback = {
                "category_id": category["id"],
                "email": fake.email(),
                "mobile_phone": "71234567890",
                "title": f"#{count_feedback}# {fake.sentence()}",
                "message": f"#{count_feedback}# {fake.text(max_nb_chars=250)}",
            }
            feedback_controller.create(new_feedback)

    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.warning(f"Load init data | error load feedback | {repr(e)}")


def load_fake_data() -> None:
    """Load fake data for frontends clients."""
    _load_articles(articles)
    _load_feedbacks()
