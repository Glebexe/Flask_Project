import os
from app.models import User, Company, Job
from app import create_app, db
from flask_migrate import Migrate
import unittest

flask_app = create_app('default')
migrate = Migrate(flask_app, db)

#
# @flask_app.shell_context_processors
# def make_shell_contex():
#     return dict(db=db, User=User, Company=Company, Job=Job)


@flask_app.cli.command("test")
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    flask_app.run()
