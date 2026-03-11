from src.server.factory import celery_init_app, create_app


def test_celery_init_app_once():
    app = create_app(__name__)
    celery = celery_init_app(app)
    assert celery is app.extensions["celery"]
