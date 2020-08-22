from datetime import date

from flask import Flask, g, request
from flask import send_from_directory, jsonify
from flask.json import JSONEncoder
from playhouse.shortcuts import model_to_dict

from . import db, config
from .db import Job


class CustomJSONEncoder(JSONEncoder):
    """A JSON encoder that sensibly handles dates."""
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(
    __name__,
    static_folder=config.STATIC_PATH,
    static_url_path='/static',
)
app.config.from_object(__name__)
app.json_encoder = CustomJSONEncoder


@app.before_request
def before_request():
    g.db = db.database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/api/job', methods=['POST'])
def create():
    r = Job.create(
        user=request.json['user'],
        job_type='greet',
        params={'name': request.json['name'], 'msg': request.json['msg']},
    )
    return jsonify(model_to_dict(r))


@app.route('/api/jobs/<job_id>', methods=['GET'])
def job(job_id):
    return jsonify(model_to_dict(Job.get_by_id(job_id), backrefs=True))


@app.route('/api/jobs', methods=['GET'])
def jobs():
    return jsonify([
        model_to_dict(d, backrefs=True) for d in
        Job.select().order_by(Job.id.desc())
    ])


# Custom static data
@app.route('/assets/<path:filename>')
def custom_static(filename):
    return send_from_directory(config.ASSETS_PATH, filename)


@app.route('/')
@app.route('/jobs/<job_id>')
def index(job_id=None):
    return send_from_directory(app.static_folder, 'index.html')


def main():
    db.create_tables()
    if config.DEV:
        db.create_dev_data()
    app.run(debug=True, host='0.0.0.0', port=config.PORT)


if __name__ == '__main__':
    main()
