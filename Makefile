


.ONESHELL:
SHELL=/bin/bash
tests:
	python << EOF
	import unittest
	import waveshare.tests
	suite = unittest.TestLoader().loadTestsFromTestCase(waveshare.tests.TestCommandSerialization)
	unittest.TextTestRunner(verbosity=2).run(suite)
	EOF

