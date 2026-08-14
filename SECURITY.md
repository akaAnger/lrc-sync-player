# Security policy

## Supported versions

LRC Sync Player is an early-stage project. Security fixes are applied to the latest code on the `main` branch. Older commits and forks are not maintained as separate supported releases.

## Reporting a vulnerability

Please do not publish exploit details in a public issue before there is a reasonable opportunity to review and fix the problem.

Use GitHub's private vulnerability reporting feature when it is available for this repository. If private reporting is unavailable, open a public issue containing only a minimal description and a request for a private contact channel; avoid including proof-of-concept payloads, sensitive files, credentials, or personal data.

A useful report includes:

- the affected version or commit;
- the operating system and Python version;
- clear reproduction steps;
- the expected and observed behavior;
- the security impact;
- any suggested mitigation, if known.

## Scope

Issues are especially relevant when they involve unsafe handling of local paths or files, unexpected command execution, dependency or packaging problems, or behavior that exposes data beyond what the README describes.

LRC Sync Player processes local audio and LRC files. Reports about untrusted files should demonstrate an impact beyond a normal parse or playback error.

## Dependencies

The project relies on `pygame` and `rich`. Vulnerabilities that originate entirely in a dependency should also be reported to that dependency's maintainers, while an issue here may be appropriate if LRC Sync Player needs to pin, upgrade, or work around the affected version.
