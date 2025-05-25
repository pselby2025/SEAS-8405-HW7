# Threat Model – Flask App

## STRIDE Analysis

| Threat | Description | Example |
|--------|-------------|---------|
| Spoofing | No auth on routes | Unverified access to `/ping` |
| Tampering | Input abuse on `/calculate` | Literal evaluation of user input |
| Repudiation | No audit trail | No logs or access control |
| Information Disclosure | Stack traces, error messages | Ping failure or eval crash |
| Denial of Service | Repeated `ping` usage | May slow or crash the server |
| Elevation of Privilege | No role separation | All users can execute sensitive endpoints |

---

## MITRE ATT&CK for Containers (Relevant Techniques)

- **T1203** – Exploitation for Client Execution (`eval`)
- **T1059** – Command Execution (`subprocess`)
- **T1499** – Denial of Service (ping spam)
- **T1611** – Escape to Host (subprocess risks)

---

## Vulnerabilities to NIST 800-53 Controls

| Vulnerability | NIST Control | Summary |
|---------------|--------------|---------|
| `eval()` | SI-10 | Input validation & code execution restriction |
| `subprocess` usage | SI-3, SI-7 | Restrict script access to OS |
| No Auth | AC-2, IA-2 | Identity enforcement |
| Full error return | SI-11, SC-12 | Sanitize and limit feedback |
| `/ping` overload | SC-5, IR-4 | Monitor and restrict request abuse |
