import unittest

from .test_tosca_base import Test_Orchestrator


class Test_Dockerfile(Test_Orchestrator):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.file = 'data/examples/dockerfile/hello-dockerfile.yaml'

    def test(self):
        self.create()
        self.start_check_exit()
        self.stop()
        self.start_check_exit()
        self.stop()
        self.delete()


if __name__ == '__main__':
    unittest.main()
