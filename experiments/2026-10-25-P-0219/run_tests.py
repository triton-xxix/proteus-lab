"""Run the repo's own audit tests (it ships no tests/__init__.py, so discovery refuses the folder)."""
import sys, unittest
root = "/Users/triton/PROTEUS/sandbox/p0219-kinship/ex-ussr-kinship-research-main"
sys.path.insert(0, root)
sys.path.insert(0, root + "/tests")
import test_audit_evidence
suite = unittest.defaultTestLoader.loadTestsFromModule(test_audit_evidence)
r = unittest.TextTestRunner(verbosity=2).run(suite)
print("ran", r.testsRun, "failures", len(r.failures), "errors", len(r.errors))
