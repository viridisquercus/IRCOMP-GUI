# Working changes

Keep changes in logical, recoverable commits. Separate research, design, domain
behavior, transport and visual integration when each has a coherent result.
Commit messages describe the change, not the editing tool or conversation.

Before a commit, inspect the diff and run checks appropriate to that change.
Do not include credentials, runtime databases, unrelated work or generated caches.
Preserve existing history; use a new corrective commit or `git revert` for a
published change rather than rewriting a shared branch.

For the current repository work, publish completed verified task increments to
`origin` so the GitHub view matches the local result. Check the remote before
pushing; reconcile concurrent changes instead of force-pushing. Report commit
identifiers and any publication failure. Never imply a local commit is published.

Research and design commits may contain review TODOs. Distinguish pending
validation from implemented or tested behavior in every milestone record.
