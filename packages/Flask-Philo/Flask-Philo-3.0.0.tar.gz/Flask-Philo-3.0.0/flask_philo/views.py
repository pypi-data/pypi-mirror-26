from flask_philo import app
from flask import abort, json, render_template, make_response, Response, g
from flask.views import MethodView


class BaseView(MethodView):
    def __init__(self, *args, **kwargs):

        # assign postgresql pool connections
        if 'DATABASES' in app.config and\
                'POSTGRESQL' in app.config['DATABASES']:
            if hasattr(g, 'postgresql_pool'):
                self.postgresql_pool = g.postgresql_pool

        # assign redis pool connections
        if 'DATABASES' in app.config and 'REDIS' in app.config['DATABASES']:
            if hasattr(g, 'redis_pool'):
                self.redis_pool = g.redis_pool

        super(BaseView, self).__init__(*args, **kwargs)

    def json_response(self, status=200, data={}, headers={}):
        mimetype = 'application/json'

        return Response(
            json.dumps(data),
            status=status,
            mimetype=mimetype,
            headers=headers)

    def render_template(self, template_name, **values):
        return render_template(template_name, **values)

    def template_response(self, template_name, headers={}):  # noqa
        """
        Constructs a response, allowing custom template name and content_type
        """
        response = make_response(render_template(template_name))

        for field, value in headers.items():
            response.headers.set(field, value)

        return response

    def get(self, *args, **kwargs):
        abort(400)

    def post(self, *args, **kwargs):
        abort(400)

    def put(self, *args, **kwargs):
        abort(400)

    def patch(self, *args, **kwargs):
        abort(400)

    def delete(self, *args, **kwargs):
        abort(400)


class BaseResourceView(BaseView):

    def get(self, *args, **kwargs):
        return self.json_response(400)

    def post(self, *args, **kwargs):
        return self.json_response(400)

    def put(self, *args, **kwargs):
        return self.json_response(400)

    def patch(self, *args, **kwargs):
        return self.json_response(400)

    def delete(self, *args, **kwargs):
        return self.json_response(400)
