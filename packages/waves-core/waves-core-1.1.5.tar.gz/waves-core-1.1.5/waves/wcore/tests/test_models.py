""" WAVES models Tests cases """
from __future__ import unicode_literals

import logging
import os

from django.test import TestCase
from django.utils.module_loading import import_string

import waves.wcore.adaptors.const
from waves.wcore.adaptors.adaptor import JobAdaptor
from waves.wcore.models import get_service_model, get_submission_model
from waves.wcore.tests.base import WavesBaseTestCase
from waves.wcore.tests.tests_utils import create_runners, create_service_for_runners

logger = logging.getLogger(__name__)
Service = get_service_model()
Submission = get_submission_model()


class TestRunner(TestCase):
    def test_create_runner(self):
        for runner in create_runners():
            logger.info('Current: %s - %s', runner.name, runner.clazz)
            adaptor = runner.adaptor
            self.assertIsInstance(adaptor, JobAdaptor)
            self.assertEqual(runner.run_params.__len__(), adaptor.init_params.__len__())
            self.assertListEqual(sorted(runner.run_params.keys()), sorted(adaptor.init_params.keys()))
            obj_runner = import_string(runner.clazz)
            expected_params = obj_runner().init_params
            runner_params = runner.run_params
            logger.debug("Expected %s", expected_params)
            logger.debug("Defaults %s", runner_params)
            self.assertEquals(sorted(expected_params), sorted(runner_params))


class TestServices(WavesBaseTestCase):
    def test_create_service(self):
        for service in create_service_for_runners():
            self.assertEqual(service.submissions.count(), 1)
            # Assert that service params has a length corresponding to 'allowed override' value
            self.assertListEqual(sorted(service.run_params.keys()), sorted(service.runner.run_params.keys()))

    def test_load_service(self):
        from waves.wcore.models.serializers.services import ServiceSerializer
        import json
        init_count = Service.objects.all().count()
        file_paths = []
        for srv in Service.objects.all():
            file_paths.append(srv.serialize())
        for exp in file_paths:
            with open(exp) as fp:
                serializer = ServiceSerializer(data=json.load(fp))
                if serializer.is_valid():
                    serializer.save()
        self.assertEqual(init_count * 2, Service.objects.all().count())


class TestJobs(WavesBaseTestCase):

    def test_jobs_signals(self):
        job = self._create_random_job()
        self.assertIsNotNone(job.title)
        self.assertEqual(job.outputs.count(), 4)
        self.assertTrue(os.path.isdir(job.working_dir))
        logger.debug('Job directories has been created %s ', job.working_dir)
        self.assertEqual(job.status, waves.wcore.adaptors.const.JOB_CREATED)
        self.assertEqual(job.job_history.count(), 1)
        job.message = "Test job Message"
        job.status = waves.wcore.adaptors.const.JOB_PREPARED
        job.save()
        self.assertGreaterEqual(job.job_history.filter(message__contains=job.message).all(), 0)
        job.delete()
        self.assertFalse(os.path.isdir(job.working_dir))
        logger.debug('Job directories has been deleted')

    def test_job_history(self):
        job = self._create_random_job()
        job.job_history.create(message="Test Admin message", status=job.status, is_admin=True)
        job.job_history.create(message="Test public message", status=job.status)
        try:
            self.assertEqual(job.job_history.count(), 3)
            self.assertEqual(job.public_history.count(), 2)
        except AssertionError:
            logger.debug('All history %s', job.job_history.all())
            logger.debug('Public history %s', job.public_history.all())
            raise
