import unittest

import boto3
from moto import mock_ecs
from testfixtures import LogCapture

from stacker.hooks.ecs import create_clusters

REGION = "us-east-1"


class TestECSHooks(unittest.TestCase):
    def test_create_single_cluster(self):
        with mock_ecs():
            cluster = "test-cluster"
            logger = "stacker.hooks.ecs"
            client = boto3.client("ecs", region_name=REGION)
            response = client.list_clusters()

            self.assertEqual(len(response["clusterArns"]), 0)
            with LogCapture(logger) as logs:
                self.assertTrue(
                    create_clusters(
                        region=REGION,
                        namespace="fake",
                        mappings={},
                        parameters={},
                        clusters=cluster
                    )
                )

                logs.check(
                    (
                        logger,
                        "DEBUG",
                        "Creating ECS cluster: %s" % cluster
                    )
                )

            response = client.list_clusters()
            self.assertEqual(len(response["clusterArns"]), 1)

    def test_create_multiple_clusters(self):
        with mock_ecs():
            clusters = ("test-cluster0", "test-cluster1")
            logger = "stacker.hooks.ecs"
            client = boto3.client("ecs", region_name=REGION)
            response = client.list_clusters()

            self.assertEqual(len(response["clusterArns"]), 0)
            for cluster in clusters:
                with LogCapture(logger) as logs:
                    self.assertTrue(
                        create_clusters(
                            region=REGION,
                            namespace="fake",
                            mappings={},
                            parameters={},
                            clusters=cluster
                        )
                    )

                    logs.check(
                        (
                            logger,
                            "DEBUG",
                            "Creating ECS cluster: %s" % cluster
                        )
                    )

            response = client.list_clusters()
            self.assertEqual(len(response["clusterArns"]), 2)
