from unittest import mock
import sys
import pytest
from grpc import StatusCode

from orator.exceptions.orm import (ModelNotFound, RelatedClassNotFound,
                                   ValidationError)
from sea.contrib.extensions import orator
from sea.contrib.extensions.orator import cli
from sea.contrib.extensions.orator.middleware import OratorExceptionMiddleware
from sea.test.stub import Context


def test_orator(app):
    c = orator.Orator()
    assert c._dbmanager is None
    c.init_app(app)
    assert isinstance(c._dbmanager, orator.orator.DatabaseManager)
    with mock.patch.object(c._dbmanager, 'connection') as mocked:
        c.connection()
        mocked.assert_called_once_with()


def test_model_meta(cache, db):
    from app.models import User

    assert hasattr(User, 'find_by')

    jack = User.create(username='jack', age=35)
    key = User.find_by.make_cache_key(User, 'username', 'jack')
    assert not cache.exists(key)
    assert User.find_by('username', 'jack').id == jack.id
    assert cache.exists(key)

    jane = User.create(username='jane', age=31)
    assert User.find(jane.id).username == jane.username
    key = User.find.make_cache_key(User, jane.id)
    assert cache.exists(key)
    jane.husband().associate(jack)
    jane.save()
    assert not cache.exists(key)

    assert User.find_or_fail(jack.id).username == jack.username
    with pytest.raises(ModelNotFound):
        User.find_or_fail(0)
    assert User.find_by_or_fail('username', jack.username).id == jack.id
    with pytest.raises(ModelNotFound):
        User.find_by_or_fail('username', 'no')

    c1 = User.create(username='c1', age=5)
    c2 = User.create(username='c2', age=2)
    k1 = User.find.make_cache_key(User, c1.id)
    k2 = User.find.make_cache_key(User, c2.id)
    User.find(c1.id)
    assert cache.exists(k1)
    assert not cache.exists(k2)
    children = User.find([c1.id, c2.id])
    assert cache.exists(k2)
    assert len(children) == 2
    with mock.patch('sea.contrib.extensions.orator.cache_model._bulk_register_to_related_caches') as mocked:
        User.find([c1.id, c2.id])
        assert not mocked.called
    jack.children().save_many([c1, c2])
    assert not cache.exists(k1)
    assert not cache.exists(k2)

    assert User.find(1000) is None
    assert len(User.find([c1.id, 2000])) == 1


def test_cli(app):
    sys.argv = ['seaorator', '-h']
    with pytest.raises(SystemExit):
        cli.main()

    with mock.patch('sea.contrib.extensions.orator.cli.application'):
        with mock.patch.object(app, 'root_path', new='.'):
            sys.argv = 'seaorator help'.split()
            cli.main()
            assert sys.argv == 'orator help'.split()

            sys.argv = 'seaorator list'.split()
            cli.main()
            assert sys.argv == 'orator list'.split()

            sys.argv = 'seaorator migrate'.split()
            cli.main()
            assert sys.argv[1] == 'migrate'
            argv = ' '.join(sys.argv)
            assert '--config ./configs/default/orator.py' in argv
            assert '--path ./db/migrations' in argv

            sys.argv = 'seaorator db:seed'.split()
            cli.main()
            assert sys.argv[1] == 'db:seed'
            argv = ' '.join(sys.argv)
            assert '--config ./configs/default/orator.py' in argv
            assert '--path ./db/seeds' in argv

            sys.argv = 'seaorator make:migration'.split()
            cli.main()
            assert sys.argv[1] == 'make:migration'
            argv = ' '.join(sys.argv)
            assert '--path ./db/migrations' in argv

            sys.argv = 'seaorator make:seed'.split()
            cli.main()
            assert sys.argv[1] == 'make:seed'
            argv = ' '.join(sys.argv)
            assert '--path ./db/seeds' in argv

            sys.argv = 'seaorator migrate:reset'.split()
            cli.main()
            assert sys.argv[1] == 'migrate:reset'
            argv = ' '.join(sys.argv)
            assert '--config ./configs/default/orator.py' in argv
            assert '--path ./db/migrations' in argv

            sys.argv = 'seaorator migrate:rollback'.split()
            cli.main()
            assert sys.argv[1] == 'migrate:rollback'
            argv = ' '.join(sys.argv)
            assert '--config ./configs/default/orator.py' in argv
            assert '--path ./db/migrations' in argv

            sys.argv = 'seaorator migrate:status'.split()
            cli.main()
            assert sys.argv[1] == 'migrate:status'
            argv = ' '.join(sys.argv)
            assert '--config ./configs/default/orator.py' in argv
            assert '--path ./db/migrations' in argv


def test_orator_exception_middleware(app):
    from app.models import User

    def orator_handler(servicer, request, context):
        if request == 0:
            raise ModelNotFound(User)
        if request == 1:
            raise RelatedClassNotFound('father')
        if request == 2:
            raise ValidationError({'general': [1, 2], 'name': 'invalid'})
        return context

    h = OratorExceptionMiddleware(app, orator_handler, orator_handler)

    ctx = Context()
    h(None, 0, ctx)
    assert ctx.code == StatusCode.NOT_FOUND

    ctx = Context()
    h(None, 1, ctx)
    assert ctx.code == StatusCode.NOT_FOUND

    ctx = Context()
    h(None, 2, ctx)
    assert ctx.code == StatusCode.INVALID_ARGUMENT
