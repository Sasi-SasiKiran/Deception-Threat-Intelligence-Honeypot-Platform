# Security Design & Threat Mitigation

## 1. Threat Model & Defensive Isolation

### Attack Vectors & Mitigations
| Threat Vector | Risk | Architectural Mitigation |
|---|---|---|
| **Decoy Compromise / RCE** | Attacker exploits decoy code | Decoy is containerized with non-root user, read-only FS where possible, and has no database client libraries or network route to DB |
| **Credential Exposure** | Honeypot stores attacker/victim passwords | Strict data sanitization: all submitted `password`, `pass`, `token` fields are transformed to `[REDACTED]` prior to ingest |
| **Data Tampering** | Attacker attempts to erase or modify logs | Decoy can only emit HTTP POST to Ingest. Decoy cannot query, modify, or delete existing events |
| **Ingest Spoofing** | Attacker probes Ingest directly | Ingest is attached solely to `internal-net` and rejects requests missing valid `X-Internal-Token` |
| **Denial of Service (DoS)** | Volumetric floods to honeypot | Nginx applies connection and request rate limits. Ingest API enforces maximum body limits (50KB) |

## 2. Network Topology & Boundaries
- **Public Subnet (`attacker-facing`)**: Exposed to external traffic through port 80.
- **Private Subnet (`internal-net`)**: Strictly internal. `database` does NOT publish port 5432 to host in production configurations.
- **Ingress / Egress**: The decoy has no egress internet access in production, preventing honeypot hosts from becoming DDoS reflection proxies.

## 3. Data Minimization & Privacy
- Sensitive personal data is pruned.
- IP addresses are handled as indicators of compromise (IOCs), with no personal identifying identity assumptions.
- Passwords entered in fake login forms are never stored in plain text or reversible formats.
