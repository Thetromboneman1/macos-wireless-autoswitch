# Model Promotion Framework

Date: 2026-06-23
Owner: AI Platform

## Lifecycle States

| State | Meaning | Entry Criteria | Exit Criteria |
|---|---|---|---|
| Experimental | Locally available but not trusted for workflows | Model can be loaded in a lab window | Passes basic health, benchmark, and memory review |
| Candidate | Potential production or fallback lane | Repeatable benchmark evidence and documented purpose | Passes promotion gates or is rejected |
| Production | Supported default or role model | Health, benchmark, tool-call, documentation, and rollback gates pass | Deprecated when a replacement is approved |
| Deprecated | Still available for rollback or comparison | Replacement exists or workload no longer needs it | Retired after no active dependency remains |
| Retired | Removed from active docs and startup paths | No consumers, rollback no longer required | Reintroduced only as experimental |

## Promotion Process

1. Define workload and model role.
2. Verify endpoint visibility with authenticated `/v1/models`.
3. Run benchmark governance against the current baseline.
4. Run stability evidence appropriate to the lane: smoke, one-hour, or workday soak.
5. Run tool-call validation when the model supports agent workflows.
6. Capture memory and swap before and after validation.
7. Run documentation review and update routing, lifecycle, and rollback docs.
8. Run `scripts/operations/model-governance/evaluate-promotion.py` against the evidence.

## Rollback Process

- Revert consumers to oMLX on `127.0.0.1:18080/v1`.
- Restore the four-role Gemma contract before testing alternatives.
- Stop manual lab listeners on `8002` and `8010`.
- Re-run health, drift, documentation, and benchmark comparison as needed.

## Retirement Process

1. Confirm no active config, LaunchAgent, Docker stack, or editor integration references the model.
2. Mark the model deprecated for one review cycle unless it is a broken or unsafe local artifact.
3. Archive benchmark evidence and rollback notes.
4. Remove from active routing docs and model catalog.
5. Keep secret/config pointers out of Git.
