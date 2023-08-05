# -*- coding: utf-8 -*-

import itertools
import time
import unittest

from ..compat import cPickle
from ..util import encode_session_payload, int_time, LAZYCREATE_SESSION
from ..exceptions import InvalidSession, InvalidSession_PayloadTimeout, InvalidSession_PayloadLegacy


class TestRedisSession(unittest.TestCase):
    def _makeOne(self, redis, session_id, new, new_session,
                 serialize=cPickle.dumps, deserialize=cPickle.loads,
                 detect_changes=True, ):
        from ..session import RedisSession
        return RedisSession(
            redis=redis,
            session_id=session_id,
            new=new,
            new_session=new_session,
            serialize=serialize,
            deserialize=deserialize,
            detect_changes=detect_changes,
        )

    def _set_up_session_in_redis(self, redis, session_id, timeout,
                                 session_dict=None, serialize=cPickle.dumps):
        if session_dict is None:
            session_dict = {}
        time_now = int_time()
        expires = time_now + timeout if timeout else None
        payload = encode_session_payload(session_dict, time_now, timeout, expires)
        redis.set(session_id,
                  serialize(payload)
                  )
        return session_id

    def _make_id_generator(self):
        ids = itertools.count(start=0, step=1)
        return lambda: str(next(ids))

    def _set_up_session_in_Redis_and_makeOne(self, session_id=None,
                                             session_dict=None, new=True,
                                             timeout=300, detect_changes=True):
        from . import DummyRedis
        redis = DummyRedis()
        id_generator = self._make_id_generator()
        if session_id is None:
            session_id = id_generator()
        self._set_up_session_in_redis(redis=redis, session_id=session_id,
                                      session_dict=session_dict,
                                      timeout=timeout)
        new_session = lambda: self._set_up_session_in_redis(
            redis=redis,
            session_id=id_generator(),
            session_dict=session_dict,
            timeout=timeout,
        )
        return self._makeOne(
            redis=redis,
            session_id=session_id,
            new=new,
            new_session=new_session,
            detect_changes=detect_changes,
        )

    def test_init_new_session(self):
        session_id = 'session_id'
        new = True
        timeout = 300
        inst = self._set_up_session_in_Redis_and_makeOne(
            session_id=session_id,
            new=new,
            timeout=timeout,
        )
        self.assertEqual(inst.session_id, session_id)
        self.assertIs(inst.new, new)
        self.assertDictEqual(dict(inst), {})

    def test_init_existing_session(self):
        session_id = 'session_id'
        session_dict = {'key': 'value'}
        new = False
        timeout = 300
        inst = self._set_up_session_in_Redis_and_makeOne(
            session_id=session_id,
            session_dict=session_dict,
            new=new,
            timeout=timeout,
        )
        self.assertEqual(inst.session_id, session_id)
        self.assertIs(inst.new, new)
        self.assertDictEqual(dict(inst), session_dict)

    def test_delitem(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['key'] = 'val'
        del inst['key']
        inst.do_persist()
        session_dict_in_redis = inst.from_redis()['m']
        self.assertNotIn('key', inst)
        self.assertNotIn('key', session_dict_in_redis)

    def test_setitem(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['key'] = 'val'
        inst.do_persist()
        session_dict_in_redis = inst.from_redis()['m']
        self.assertIn('key', inst)
        self.assertIn('key', session_dict_in_redis)

    def test_getitem(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['key'] = 'val'
        inst.do_persist()
        session_dict_in_redis = inst.from_redis()['m']
        self.assertEqual(inst['key'], session_dict_in_redis['key'])

    def test_contains(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['key'] = 'val'
        inst.do_persist()
        session_dict_in_redis = inst.from_redis()['m']
        self.assertTrue('key' in inst)
        self.assertTrue('key' in session_dict_in_redis)

    def test_setdefault(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        result = inst.setdefault('key', 'val')
        self.assertEqual(result, inst['key'])

    def test_keys(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['key1'] = ''
        inst['key2'] = ''
        inst_keys = inst.keys()
        inst.do_persist()
        session_dict_in_redis = inst.from_redis()['m']
        persisted_keys = session_dict_in_redis.keys()
        self.assertEqual(inst_keys, persisted_keys)

    def test_items(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['a'] = 1
        inst['b'] = 2
        inst_items = inst.items()
        inst.do_persist()
        session_dict_in_redis = inst.from_redis()['m']
        persisted_items = session_dict_in_redis.items()
        self.assertEqual(inst_items, persisted_items)

    def test_clear(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['a'] = 1
        inst.clear()
        session_dict_in_redis = inst.from_redis()['m']
        self.assertNotIn('a', inst)
        self.assertNotIn('a', session_dict_in_redis)

    def test_get(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['key'] = 'val'
        get_from_inst = inst.get('key')
        self.assertEqual(get_from_inst, 'val')
        inst.do_persist()
        session_dict_in_redis = inst.from_redis()['m']
        get_from_redis = session_dict_in_redis.get('key')
        self.assertEqual(get_from_inst, get_from_redis)

    def test_get_default(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        get_from_inst = inst.get('key', 'val')
        self.assertEqual(get_from_inst, 'val')
        session_dict_in_redis = inst.from_redis()['m']
        get_from_redis = session_dict_in_redis.get('key', 'val')
        self.assertEqual(get_from_inst, get_from_redis)

    def test_pop(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['key'] = 'val'
        popped = inst.pop('key')
        self.assertEqual(popped, 'val')
        session_dict_in_redis = inst.from_redis()['m']
        self.assertNotIn('key', session_dict_in_redis)

    def test_pop_default(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        popped = inst.pop('key', 'val')
        self.assertEqual(popped, 'val')

    def test_update(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['a'] = 1
        to_be_updated = {'a': 'overriden', 'b': 2}
        inst.update(to_be_updated)
        self.assertEqual(inst['a'], 'overriden')
        self.assertEqual(inst['b'], 2)
        inst.do_persist()
        session_dict_in_redis = inst.from_redis()['m']
        self.assertEqual(session_dict_in_redis['a'], 'overriden')
        self.assertEqual(session_dict_in_redis['b'], 2)

    def test_iter(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        keys = ['a', 'b', 'c']
        for k in keys:
            inst[k] = k
        itered = list(inst.__iter__())
        itered.sort()
        self.assertEqual(keys, itered)

    def test_has_key(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['actual_key'] = ''
        self.assertIn('actual_key', inst)
        self.assertNotIn('not_a_key', inst)

    def test_values(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['a'] = 1
        inst['b'] = 2
        expected_values = [1, 2]
        actual_values = sorted(inst.values())
        self.assertEqual(actual_values, expected_values)

    def test_itervalues(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['a'] = 1
        inst['b'] = 2
        itered = list(inst.itervalues())
        itered.sort()
        expected = [1, 2]
        self.assertEqual(expected, itered)

    def test_iteritems(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['a'] = 1
        inst['b'] = 2
        itered = list(inst.iteritems())
        itered.sort()
        expected = [('a', 1), ('b', 2)]
        self.assertEqual(expected, itered)

    def test_iterkeys(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['a'] = 1
        inst['b'] = 2
        itered = list(inst.iterkeys())
        itered.sort()
        expected = ['a', 'b']
        self.assertEqual(expected, itered)

    def test_popitem(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['a'] = 1
        inst['b'] = 2
        popped = inst.popitem()
        options = [('a', 1), ('b', 2)]
        self.assertIn(popped, options)
        session_dict_in_redis = inst.from_redis()['m']
        self.assertNotIn(popped, session_dict_in_redis)

    def test_IDict_instance_conforms(self):
        from pyramid.interfaces import IDict
        from zope.interface.verify import verifyObject
        inst = self._set_up_session_in_Redis_and_makeOne()
        verifyObject(IDict, inst)

    def test_created(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        created = inst.from_redis()['c']
        self.assertEqual(inst.created, created)

    def test_timeout(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        timeout = inst.from_redis()['t']
        self.assertEqual(inst.timeout, timeout)

    def test_invalidate(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        first_session_id = inst.session_id
        inst.invalidate()
        self.assertNotIn(first_session_id, inst.redis.store)
        self.assertIs(inst._invalidated, True)

    def test_dict_multilevel(self):
        inst = self._set_up_session_in_Redis_and_makeOne(session_id='test1')
        inst['dict'] = {'foo': {'bar': 1}}
        inst.do_persist()
        get_from_inst = inst['dict']['foo']['bar']
        self.assertEqual(get_from_inst, 1)
        session_dict_in_redis = inst.from_redis()['m']
        get_from_redis = session_dict_in_redis['dict']['foo']['bar']
        self.assertEqual(get_from_redis, 1)
        inst['dict']['foo']['bar'] = 2
        inst.do_persist()
        session_dict_in_redis2 = inst.from_redis()['m']
        get_from_redis2 = session_dict_in_redis2['dict']['foo']['bar']
        self.assertEqual(get_from_redis2, 2)

    def test_dict_multilevel_detect_changes_on(self):
        inst = self._set_up_session_in_Redis_and_makeOne(session_id='test1',
                                                         detect_changes=True,
                                                         )
        # set a base dict and ensure it worked
        inst['dict'] = {'foo': {'bar': 1}}
        inst.do_persist()
        get_from_inst = inst['dict']['foo']['bar']
        self.assertEqual(get_from_inst, 1)
        # grab the dict and edit it
        session_dict_in_redis = inst.from_redis()['m']
        get_from_redis = session_dict_in_redis['dict']['foo']['bar']
        self.assertEqual(get_from_redis, 1)
        inst['dict']['foo']['bar'] = 2
        # ensure the change was detected
        should_persist = inst._session_state.should_persist(inst)
        self.assertTrue(should_persist)

    def test_dict_multilevel_detect_changes_off(self):
        inst = self._set_up_session_in_Redis_and_makeOne(session_id='test1',
                                                         detect_changes=False,
                                                         )
        # set a base dict and ensure it worked
        inst['dict'] = {'foo': {'bar': 1}}
        inst.do_persist()
        get_from_inst = inst['dict']['foo']['bar']
        self.assertEqual(get_from_inst, 1)
        # grab the dict and edit it
        session_dict_in_redis = inst.from_redis()['m']
        get_from_redis = session_dict_in_redis['dict']['foo']['bar']
        self.assertEqual(get_from_redis, 1)
        inst['dict']['foo']['bar'] = 2
        # ensure the change was NOT detected
        should_persist = inst._session_state.should_persist(inst)
        self.assertFalse(should_persist)

    def test_new_session_after_invalidate(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        first_session_id = inst.session_id
        inst['key'] = 'value'
        inst.invalidate()
        inst.ensure_id()  # ensure we have an id in redis, which creates a null payload
        second_session_id = inst.session_id
        self.assertSetEqual(set(inst.redis.store.keys()), {second_session_id})
        self.assertNotEqual(second_session_id, first_session_id)
        self.assertIs(bool(second_session_id), True)
        self.assertDictEqual(dict(inst), {})
        self.assertIs(inst.new, True)
        self.assertIs(inst._invalidated, False)

    def test_session_id_access_after_invalidate_creates_new_session(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        first_session_id = inst.session_id
        inst.invalidate()

        # 1.4.x+| session_id defaults to a LAZYCREATE
        self.assertIs(inst.session_id_safecheck, None)
        self.assertIs(inst.session_id, LAZYCREATE_SESSION)

        second_session_id = inst.session_id
        self.assertNotEqual(second_session_id, first_session_id)
        self.assertIs(bool(second_session_id), True)

    def test_managed_dict_access_after_invalidate_creates_new_session(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        first_session_id = inst.session_id
        inst.invalidate()
        inst.managed_dict  # access

        # 1.4.x+| session_id defaults to a LAZYCREATE
        # 1.4.x+| session_id is only created via ensure_id()
        self.assertIs(inst.session_id_safecheck, None)
        self.assertIs(inst.session_id, LAZYCREATE_SESSION)
        inst.ensure_id()

        # ORIGINALLY
        # .session_id attribute access also creates a new session after
        # invalidate, so just asserting .session_id is not enough to prove that
        # a new session was created after .managed_dict access. Here we note
        # down the session_ids in Redis right after .managed_dict access for an
        # additional check.
        session_ids_in_redis = inst.redis.store.keys()
        second_session_id = inst.session_id
        self.assertSetEqual(set(session_ids_in_redis),
                            {second_session_id})
        self.assertNotEqual(second_session_id, first_session_id)
        self.assertIs(bool(second_session_id), True)

    def test_created_access_after_invalidate_creates_new_session(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        first_session_id = inst.session_id
        inst.invalidate()
        inst.created  # access

        # 1.4.x+| session_id defaults to a LAZYCREATE
        # 1.4.x+| session_id is only created via ensure_id()
        self.assertIs(inst.session_id_safecheck, None)
        self.assertIs(inst.session_id, LAZYCREATE_SESSION)
        inst.ensure_id()

        # ORIGINALLY
        # .session_id attribute access also creates a new session after
        # invalidate, so just asserting .session_id was not enough to prove that
        # a new session was created after .created access. Here we noted down
        # the session_ids in Redis right after .created access for an
        # additional check.
        session_ids_in_redis = inst.redis.store.keys()
        second_session_id = inst.session_id
        self.assertSetEqual(set(session_ids_in_redis),
                            {second_session_id})
        self.assertNotEqual(second_session_id, first_session_id)
        self.assertIs(bool(second_session_id), True)

    def test_timeout_access_after_invalidate_creates_new_session(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        first_session_id = inst.session_id
        inst.invalidate()
        inst.timeout  # access

        # 1.4.x+| session_id defaults to a LAZYCREATE
        # 1.4.x+| session_id is only created via ensure_id()
        self.assertIs(inst.session_id_safecheck, None)
        self.assertIs(inst.session_id, LAZYCREATE_SESSION)
        inst.ensure_id()

        # ORIGINALLY:
        # .session_id attribute access also creates a new session after
        # invalidate, so just asserting .session_id is not enough to prove that
        # a new session was created after .timeout access. Here we note down
        # the session_ids in Redis right after .timeout access for an
        # additional check.
        session_ids_in_redis = inst.redis.store.keys()
        second_session_id = inst.session_id
        self.assertSetEqual(set(session_ids_in_redis),
                            {second_session_id})
        self.assertNotEqual(second_session_id, first_session_id)
        self.assertIs(bool(second_session_id), True)

    def test_new_attribute_access_after_invalidate_creates_new_session(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        first_session_id = inst.session_id
        inst.invalidate()
        inst.new  # access

        # 1.4.x+| session_id defaults to a LAZYCREATE
        # 1.4.x+| session_id is only created via ensure_id()
        self.assertIs(inst.session_id_safecheck, None)
        self.assertIs(inst.session_id, LAZYCREATE_SESSION)
        inst.ensure_id()

        # ORIGINALLY
        # .session_id attribute access also creates a new session after
        # invalidate, so just asserting .session_id is not enough to prove that
        # a new session was created after .created access. Here we note down
        # session_ids in Redis right after .new access for an additional check.
        session_ids_in_redis = inst.redis.store.keys()
        second_session_id = inst.session_id
        self.assertSetEqual(set(session_ids_in_redis),
                            {second_session_id})
        self.assertNotEqual(second_session_id, first_session_id)
        self.assertIs(bool(second_session_id), True)

    def test_repeated_invalidates_without_new_session_created_in_between(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        first_session_id = inst.session_id
        inst.invalidate()
        inst.invalidate()
        self.assertNotIn(first_session_id, inst.redis.store)
        self.assertIs(inst._invalidated, True)
        second_session_id = inst.session_id
        self.assertNotEqual(second_session_id, first_session_id)
        self.assertIs(bool(second_session_id), True)

    def test_invalidate_new_session_invalidate(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst.invalidate()
        second_session_id = inst.session_id
        inst.invalidate()
        session_ids_in_redis = inst.redis.store.keys()
        self.assertNotIn(second_session_id, session_ids_in_redis)
        self.assertIs(inst._invalidated, True)

    def test_invalidate_new_session_invalidate_new_session(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst.ensure_id()  # ensure we have an id in redis, which creates a null payload

        inst.invalidate()
        inst.ensure_id()  # ensure we have an id in redis, which creates a null payload
        second_session_id = inst.session_id

        inst.invalidate()
        inst.ensure_id()  # ensure we have an id in redis, which creates a null payload
        third_session_id = inst.session_id

        session_ids_in_redis = inst.redis.store.keys()
        self.assertSetEqual(set(session_ids_in_redis),
                            {third_session_id})
        self.assertNotEqual(third_session_id, second_session_id)
        self.assertIs(bool(third_session_id), True)
        self.assertDictEqual(dict(inst), {})
        self.assertIs(inst.new, True)
        self.assertIs(inst._invalidated, False)

    def test_mutablevalue_changed(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst['a'] = {'1': 1, '2': 2, }
        tmp = inst['a']
        tmp['3'] = 3
        inst.changed()
        inst.do_persist()
        session_dict_in_redis = inst.from_redis()['m']
        self.assertEqual(session_dict_in_redis['a'], {'1': 1, '2': 2, '3': 3, })

    def test_csrf_token(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        new_token = inst.new_csrf_token()
        got_token = inst.get_csrf_token()
        self.assertEqual(new_token, got_token)

    def test_get_new_csrf_token(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        self.assertNotIn('_csrft_', inst)
        token = inst.get_csrf_token()
        self.assertEqual(inst['_csrft_'], token)

    def test_flash(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst.flash('message')
        msgs = inst.peek_flash()
        self.assertIn('message', msgs)

    def test_flash_alternate_queue(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst.flash('message', 'queue')
        default_queue = inst.peek_flash()
        self.assertNotIn('message', default_queue)
        other_queue = inst.peek_flash('queue')
        self.assertIn('message', other_queue)

    def test_pop_flash(self):
        inst = self._set_up_session_in_Redis_and_makeOne()
        inst.flash('message')
        popped = inst.pop_flash()
        self.assertIn('message', popped)
        msgs = inst.peek_flash()
        self.assertEqual(msgs, [])

    def test_ISession_instance_conforms(self):
        from pyramid.interfaces import ISession
        from zope.interface.verify import verifyObject
        inst = self._set_up_session_in_Redis_and_makeOne()
        verifyObject(ISession, inst)

    def test_adjust_timeout_for_session(self):
        inst = self._set_up_session_in_Redis_and_makeOne(timeout=100)
        adjusted_timeout = 200
        inst.adjust_timeout_for_session(adjusted_timeout)
        inst.do_persist()
        self.assertEqual(inst.timeout, adjusted_timeout)
        self.assertEqual(inst.from_redis()['t'], adjusted_timeout)


class TestRedisSessionNew(unittest.TestCase):
    """these are 1.2x+ tests"""

    def _makeOne(self, redis, session_id, new, new_session,
                 serialize=cPickle.dumps, deserialize=cPickle.loads,
                 detect_changes=True, set_redis_ttl=True, ):
        from ..session import RedisSession
        return RedisSession(
            redis=redis,
            session_id=session_id,
            new=new,
            new_session=new_session,
            serialize=serialize,
            deserialize=deserialize,
            detect_changes=detect_changes,
            set_redis_ttl=set_redis_ttl,
        )

    def _set_up_session_in_redis(self, redis, session_id, timeout,
                                 session_dict=None, serialize=cPickle.dumps,
                                 session_version=None, expires=None):
        if session_dict is None:
            session_dict = {}

        payload = encode_session_payload(session_dict, int_time(), timeout, expires)
        if session_version is not None:
            payload['v'] = session_version
        if expires is not None:
            payload['x'] = expires
        redis.set(session_id, serialize(payload))
        redis._history_reset()
        return session_id

    def _make_id_generator(self):
        ids = itertools.count(start=0, step=1)
        return lambda: str(next(ids))

    def _set_up_session_in_Redis_and_makeOne(self, session_id=None,
                                             session_dict=None, new=True,
                                             timeout=60, detect_changes=True,
                                             set_redis_ttl=True, session_version=None,
                                             expires=None):
        from . import DummyRedis
        redis = DummyRedis()
        id_generator = self._make_id_generator()
        if session_id is None:
            session_id = id_generator()
        self._set_up_session_in_redis(redis=redis, session_id=session_id,
                                      session_dict=session_dict,
                                      timeout=timeout,
                                      session_version=session_version,
                                      expires=expires)
        new_session = lambda: self._set_up_session_in_redis(
            redis=redis,
            session_id=id_generator(),
            session_dict=session_dict,
            timeout=timeout,
        )
        return self._makeOne(
            redis=redis,
            session_id=session_id,
            new=new,
            new_session=new_session,
            detect_changes=detect_changes,
            set_redis_ttl=set_redis_ttl,
        )

    def _deserialize_session(self, session, deserialize=cPickle.loads):
        _session_id = session.session_id
        _session_data = session.redis.store[_session_id]
        _session_serialized = deserialize(_session_data)
        return _session_serialized

    def test_init_new_session_notimeout(self):
        session_id = 'session_id'
        new = True
        timeout = 0
        set_redis_ttl = True
        session = self._set_up_session_in_Redis_and_makeOne(
            session_id=session_id,
            new=new,
            timeout=timeout,
            set_redis_ttl=set_redis_ttl,
        )
        session.do_persist()  # trigger the real session's set/setex
        self.assertEqual(session.session_id, session_id)
        self.assertIs(session.new, new)
        self.assertDictEqual(dict(session), {})

        self.assertEqual(session.timeout, None)

        _deserialized = self._deserialize_session(session)
        self.assertNotIn('t', _deserialized)

        self.assertEqual(len(session.redis._history), 1)
        _redis_op = session.redis._history[0]
        self.assertEqual(_redis_op[0], 'set')

        # clear the history, `do_refresh` should do nothing (timeout=0)
        session.redis._history_reset()
        session.do_refresh()  # trigger the real session's set/setex
        self.assertEqual(len(session.redis._history), 0)  # we shouldn't have any timeout at all

        # clear the history, `do_refresh+force_redis_ttl` ensures an "expire"
        session.redis._history_reset()
        session.do_refresh(force_redis_ttl=47)  # trigger the real session's set/setex
        self.assertEqual(len(session.redis._history), 1)
        _redis_op = session.redis._history[0]
        self.assertEqual(_redis_op[0], 'expire')
        self.assertEqual(_redis_op[2], 47)

    def test_init_new_session_notimeout_lru(self):
        """
        check that a no timeout will trigger a SET if LRU enabled
        """
        session_id = 'session_id'
        new = True
        timeout = 0
        set_redis_ttl = False
        session = self._set_up_session_in_Redis_and_makeOne(
            session_id=session_id,
            new=new,
            timeout=timeout,
            set_redis_ttl=set_redis_ttl,
        )
        session.do_persist()  # trigger the real session's set/setex
        self.assertEqual(session.session_id, session_id)
        self.assertIs(session.new, new)
        self.assertDictEqual(dict(session), {})

        _deserialized = self._deserialize_session(session)
        self.assertNotIn('t', _deserialized)
        self.assertEqual(len(session.redis._history), 1)
        _redis_op = session.redis._history[0]
        self.assertEqual(_redis_op[0], 'set')

        # clear the history, `do_refresh` should do nothing (timeout=0)
        session.redis._history_reset()
        session.do_refresh()  # trigger the real session's set/setex
        self.assertEqual(len(session.redis._history), 0)  # we shouldn't have any timeout at all

        # clear the history, `do_refresh+force_redis_ttl` ensures an "expire"
        session.redis._history_reset()
        session.do_refresh(force_redis_ttl=47)  # trigger the real session's set/setex
        self.assertEqual(len(session.redis._history), 1)
        _redis_op = session.redis._history[0]
        self.assertEqual(_redis_op[0], 'expire')
        self.assertEqual(_redis_op[2], 47)

    def test_init_new_session_timeout(self):
        """
        check that a timeout will trigger a SETEX
        """
        session_id = 'session_id'
        new = True
        timeout = 60
        set_redis_ttl = True
        session = self._set_up_session_in_Redis_and_makeOne(
            session_id=session_id,
            new=new,
            timeout=timeout,
            set_redis_ttl=set_redis_ttl,
        )
        session.do_persist()  # trigger the real session's set/setex
        self.assertEqual(session.session_id, session_id)
        self.assertIs(session.new, new)
        self.assertDictEqual(dict(session), {})

        _deserialized = self._deserialize_session(session)
        self.assertIn('t', _deserialized)
        self.assertEqual(len(session.redis._history), 1)
        _redis_op = session.redis._history[0]
        self.assertEqual(_redis_op[0], 'setex')

        # clear the history, `do_refresh` should issue an "expire" (timeout=60)
        session.redis._history_reset()
        session.do_refresh()  # trigger the real session's set/setex
        # we shouldn't have set a timeout
        self.assertEqual(len(session.redis._history), 1)
        _redis_op = session.redis._history[0]
        self.assertEqual(_redis_op[0], 'expire')

        # clear the history, `do_refresh+force_redis_ttl` ensures an "expire"
        session.redis._history_reset()
        session.do_refresh(force_redis_ttl=47)  # trigger the real session's set/setex
        self.assertEqual(len(session.redis._history), 1)
        _redis_op = session.redis._history[0]
        self.assertEqual(_redis_op[0], 'expire')
        self.assertEqual(_redis_op[2], 47)

    def test_init_new_session_timeout_lru(self):
        """
        check that a timeout will trigger a SET if LRU enabled
        """
        session_id = 'session_id'
        new = True
        timeout = 60
        set_redis_ttl = False
        session = self._set_up_session_in_Redis_and_makeOne(
            session_id=session_id,
            new=new,
            timeout=timeout,
            set_redis_ttl=set_redis_ttl,
        )
        session.do_persist()  # trigger the real session's set/setex
        self.assertEqual(session.session_id, session_id)
        self.assertIs(session.new, new)
        self.assertDictEqual(dict(session), {})
        _deserialized = self._deserialize_session(session)
        self.assertIn('t', _deserialized)
        self.assertEqual(len(session.redis._history), 1)
        _redis_op = session.redis._history[0]
        self.assertEqual(_redis_op[0], 'set')

        # clear the history, `do_refresh` should do nothing (timeout=60, set_redis_ttl=False)
        session.redis._history_reset()
        session.do_refresh()  # trigger the real session's set/setex
        self.assertEqual(len(session.redis._history), 0)

        # clear the history, `do_refresh` should issue an "expire" (force_redis_ttl=60)
        session.redis._history_reset()
        session.do_refresh(force_redis_ttl=47)  # trigger the real session's set/setex
        self.assertEqual(len(session.redis._history), 1)
        _redis_op = session.redis._history[0]
        self.assertEqual(_redis_op[0], 'expire')
        self.assertEqual(_redis_op[2], 47)

    def test_session_invalid_legacy(self):
        """
        check that ``exceptions.InvalidSession_PayloadLegacy`` is raised if a previous version is detected
        """
        session_id = 'session_id'
        new = True
        timeout = 60
        set_redis_ttl = False
        session_version = -1
        with self.assertRaises(InvalidSession_PayloadLegacy):
            session = self._set_up_session_in_Redis_and_makeOne(
                session_id=session_id,
                new=new,
                timeout=timeout,
                set_redis_ttl=set_redis_ttl,
                session_version=session_version,
            )
        return

    def test_session_invalid_expires(self):
        """
        check that ``exceptions.InvalidSession_PayloadTimeout`` is raised if we timed out
        """
        session_id = 'session_id'
        new = True
        timeout = 60
        set_redis_ttl = False
        expires = int_time() - timeout
        with self.assertRaises(InvalidSession_PayloadTimeout):
            session = self._set_up_session_in_Redis_and_makeOne(
                session_id=session_id,
                new=new,
                timeout=timeout,
                set_redis_ttl=set_redis_ttl,
                expires=expires,
            )
