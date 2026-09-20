## Repository Locations

Git repositories live in `$HOME/workspace`, one directory per repo.

## Pull Requests

Agents prepare PRs, they don't open them. Write the body to
`.opencode/pr-body.md` and give the user the `gh pr create` command to run
from the host.

## Prose Is Skill-Gated

Invoke the `prose` skill before drafting any prose meant for a human reader:

- code comments and docstrings
- commit messages
- PR titles, descriptions, review comments, and replies to review comments
- JIRA and GitHub issue titles and descriptions
- README and other documentation, user-facing error messages

Invoke it before the first word is written, not as a cleanup pass afterward.
When a more specific skill covers the format (`docstrings`, `pr-description`,
`jira-ticket`, `github-issue`, `pr-review-response`), invoke that one; it pulls
in `prose` itself.

Default to less. Pick the shortest form that carries the information, and cut
any sentence you are unsure earns its place.
