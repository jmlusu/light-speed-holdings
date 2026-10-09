Start the required application server(s) for the current task.

Follow this sequence EXACTLY:

1. Identify which server(s) need to be started.
2. Start them using the project's documented/current startup method.
3. Confirm that each server successfully starts.
4. Identify the actual port(s) and endpoint(s).
5. Perform at least one appropriate health/request check.
6. Once successfully started, monitor the server(s) continuously for EXACTLY 60 seconds.
7. During monitoring, check for:
   - crashes
   - process termination
   - startup exceptions
   - repeated errors
   - failed requests
   - obvious resource/runtime problems
8. Do NOT modify unrelated code while monitoring.
9. Stop only if required by the project's normal verification procedure or if continuing would be unsafe.

Report:

### SERVER STATUS
RUNNING / FAILED TO START / CRASHED / DEGRADED

### STARTUP
- Server:
- Command/method:
- Port:
- Startup result:

### HEALTH CHECK
- Endpoint/request:
- Result:
- Response/status:

### 60-SECOND MONITORING
- Duration actually observed:
- Crashes: YES/NO
- Errors: YES/NO
- Failed requests: YES/NO
- Other anomalies:

### FINAL RESULT
PASS / PASS WITH WARNINGS / FAIL

### EVIDENCE
Provide the relevant logs, response/status codes, process state, or other concrete evidence.

If the server cannot start, STOP the verification and report the blocker. Do not start unrelated services or begin unrelated debugging.