from flask import Flask


def register_context_handlers(app: Flask) -> Flask:
    @app.after_request
    def after_request(response):
        # Установка заголовков запроса для активации CORS.
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Accept, Authorization, Origin, Content-Type, Cache-Control",
        )
        response.headers.add("Access-Control-Expose-Headers", "Accept, Content-Disposition")
        response.headers.add(
            "Content-Security-Policy-Report-Only", "default-src 'self'; script-src 'unsafe-eval'"
        )
        return response

    return app
