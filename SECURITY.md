# Security

## Sensitive material

Do not send `.env` files, API keys, tokens, passwords, credentials, private certificates, secrets, or unauthorized business files to an external reviewer. Check the actual material, attachments, screenshots and logs before sharing. A task summary is not authorization to share its underlying files.

## Authorization scope

Authorization must bind the specific **material**, **destination** and **purpose**. Permission for one file does not cover its repository. Permission from an earlier task does not automatically cover a new task. Obtain explicit authorization before expanding any of these boundaries. Never include secrets in review material.

## Secret scanning

Secret detection is heuristic and cannot guarantee that sensitive data will always be detected. Automated checks cannot replace semantic inspection of the material and its sharing permissions. The tests contain deliberately synthetic secret-like strings for negative tests; these must remain synthetic.

## Security issues

Report authorization bypass, secret leakage, Completion Gate bypass, false external review attribution, wrong-session or wrong-round acceptance, and private material included without authorization. Provide a minimal synthetic reproduction and the affected version; omit live credentials, real conversations and private project data.

## Reporting

Open a private security report through the repository hosting platform when available. On GitHub, use **Security and quality → Report a vulnerability** if the repository has enabled private vulnerability reporting. This document alone does not enable that feature.

If no private reporting option is available, open an issue asking how to contact the maintainer privately, without vulnerability details or sensitive data. Do not post an exploit or secret in a public issue. No dedicated security email or response-time commitment is currently published.

See [GitHub's private reporting instructions](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately).
