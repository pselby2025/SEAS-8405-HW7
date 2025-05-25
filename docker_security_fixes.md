# Summary Report

## Steps Taken

1. **Initial Code Review & Static Analysis**:

   * Conducted a manual review of `app.py` and supporting Docker infrastructure.
   * Used Bandit to statically analyze the codebase for known Python security issues.

2. **Vulnerability Identification**:

   * Identified use of `subprocess`, `eval`, and insufficient input validation.
   * Ran Bandit and received flags for subprocess use, lack of shell security, and insecure path handling.

3. **Security Fixes Applied**:

   * Removed use of `eval` and replaced with `ast.literal_eval`.
   * Replaced unvalidated subprocess calls with full path calls validated using `shutil.which()`.
   * Validated IP input with `ipaddress.ip_address()` to prevent injection.
   * Updated `Dockerfile` with:

     * `USER` directive to drop root privileges
     * `HEALTHCHECK` to ensure service is running
   * Updated `docker-compose.yml` with:

     * `read_only`, `security_opt`, `mem_limit`, `pids_limit`
     * Restricted service ports to `127.0.0.1`
   * Applied hardening settings to `daemon.json` (e.g., `userns-remap`, `live-restore`, logging limits).

4. **Threat Modeling**:

   * Performed STRIDE analysis identifying spoofing, tampering, DoS, and info disclosure risks.
   * Mapped findings to MITRE ATT\&CK techniques and NIST 800-53 controls.
   * Documented threats, mitigations, and mapped controls in `threat_model.md`.

5. **Documentation and Reporting**:

   * Generated architecture diagram showing hardened Docker and app layers.
   * Scripted fixes in `docker_security_fixes.py` to automate security posture improvements.

---

## Vulnerabilities Found and Fixed

| Vulnerability                   | Fix                                                                      |
| ------------------------------- | ------------------------------------------------------------------------ |
| Use of `eval()`                 | Replaced with `ast.literal_eval()`                                       |
| Untrusted input to `subprocess` | Input validation using `ipaddress`; used full path with `shutil.which()` |
| No privilege drop in container  | Added non-root `USER` in Dockerfile                                      |
| No health monitoring            | Added `HEALTHCHECK` to Dockerfile                                        |
| Excess container permissions    | Added limits via `docker-compose.yml`                                    |
| No Docker daemon hardening      | Applied `daemon.json` with flags like `userns-remap` and `live-restore`  |

---

## Architecture and Security Improvements

* Implemented **defense in depth** via application validation, container hardening, and runtime configuration.
* Reduced risk of privilege escalation by running containers as unprivileged users.
* Minimized container attack surface with `read_only` file systems and resource limits.
* Enforced IP validation and subprocess control to mitigate command injection.
* Implemented a secure software supply chain via automation and threat modeling alignment.

---

## Reflection and Lessons Learned

* Static analysis tools like Bandit are essential for early discovery of insecure coding practices.
* Even minimal Flask apps can introduce critical risks if not sandboxed and validated.
* Docker security requires layered controls: from code to container runtime and orchestrator.
* Mapping findings to frameworks (MITRE ATT\&CK, NIST 800-53) strengthens both understanding and reporting.
* Writing automation scripts not only saves time but also enforces consistency and reproducibility in secure deployments.
