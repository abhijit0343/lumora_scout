"""
Purpose: Parser and in-memory cache loader for custom domain, IP range, and keyword blocklist files.
Inputs: Blocklist directory path (BLOCKLIST_DIR).
Outputs: Compiled sets of prohibited domains, IP networks, and regex patterns.
Dependencies: pathlib, ipaddress, app.core.config.
TODOs:
  - Read domains.txt, ip_ranges.txt, and keywords.txt from BLOCKLIST_DIR.
  - Parse domain wildcards and CIDR blocks into optimized lookup structures.
  - Provide is_blocked(domain_or_ip) lookup method.
"""
