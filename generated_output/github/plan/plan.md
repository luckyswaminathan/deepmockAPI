# Reverse Engineering Plan for `github`

**Total Routes:** 952
**Generated At:** 2025-11-11T20:05:08.945436+00:00

## Agent Directives
1. Review the component summary below to understand the CRUD surface.
2. Use component-specific plans in `plan/components/` for detailed route information.
3. Implement server handlers that satisfy the described operations and filters.
4. Raise any ambiguities called out in validation warnings before coding.

## Validation Summary
### Errors
- ⚠️ Missing component mapping for GET /advisories.
- ⚠️ Missing component mapping for POST /app-manifests/{code}/conversions.
- ⚠️ Missing component mapping for GET /app/hook/deliveries.
- ⚠️ Missing component mapping for POST /app/hook/deliveries/{delivery_id}/attempts.
- ⚠️ Missing component mapping for GET /app/installation-requests.
- ⚠️ Missing component mapping for PUT /app/installations/{installation_id}/suspended.
- ⚠️ Missing component mapping for DELETE /app/installations/{installation_id}/suspended.
- ⚠️ Missing component mapping for DELETE /applications/{client_id}/grant.
- ⚠️ Missing component mapping for DELETE /applications/{client_id}/token.
- ⚠️ Missing component mapping for GET /assignments/{assignment_id}/accepted_assignments.
- ... and 316 more errors
### Warnings
- ⚠️ No component mapping found for GET /advisories.
- ⚠️ No component mapping found for POST /app-manifests/{code}/conversions.
- ⚠️ No component mapping found for GET /app/hook/deliveries.
- ⚠️ No component mapping found for POST /app/hook/deliveries/{delivery_id}/attempts.
- ⚠️ No component mapping found for GET /app/installation-requests.
- ⚠️ No component mapping found for PUT /app/installations/{installation_id}/suspended.
- ⚠️ No component mapping found for DELETE /app/installations/{installation_id}/suspended.
- ⚠️ No component mapping found for DELETE /applications/{client_id}/grant.
- ⚠️ No component mapping found for DELETE /applications/{client_id}/token.
- ⚠️ No component mapping found for GET /assignments/{assignment_id}/accepted_assignments.
- ... and 316 more warnings

## Component Summary

Each component below has a dedicated plan file in `plan/components/` with detailed route information.

| Component | Operations | Route Count | Plan File |
|-----------|------------|-------------|-----------|
| `actions-billing-usage` | `read_one` | 2 | `plan/components/actions-billing-usage.md` |
| `actions-cache-list` | `read_one`, `delete` | 2 | `plan/components/actions-cache-list.md` |
| `actions-cache-usage-by-repository` | `read_one` | 1 | `plan/components/actions-cache-usage-by-repository.md` |
| `actions-cache-usage-org-enterprise` | `read_one` | 1 | `plan/components/actions-cache-usage-org-enterprise.md` |
| `actions-get-default-workflow-permissions` | `read_one` | 2 | `plan/components/actions-get-default-workflow-permissions.md` |
| `actions-organization-permissions` | `read_one` | 1 | `plan/components/actions-organization-permissions.md` |
| `actions-public-key` | `read_one` | 3 | `plan/components/actions-public-key.md` |
| `actions-repository-permissions` | `read_one` | 1 | `plan/components/actions-repository-permissions.md` |
| `actions-secret` | `read_one` | 2 | `plan/components/actions-secret.md` |
| `actions-set-default-workflow-permissions` | `update` | 2 | `plan/components/actions-set-default-workflow-permissions.md` |
| `actions-variable` | `read_one` | 2 | `plan/components/actions-variable.md` |
| `actions-workflow-access-to-repository` | `read_one`, `update` | 2 | `plan/components/actions-workflow-access-to-repository.md` |
| `activity` | `read_one` | 1 | `plan/components/activity.md` |
| `api-overview` | `read_many` | 1 | `plan/components/api-overview.md` |
| `artifact` | `read_one`, `delete` | 5 | `plan/components/artifact.md` |
| `authentication-token` | `create` | 4 | `plan/components/authentication-token.md` |
| `authorization` | `create`, `update_partial` | 3 | `plan/components/authorization.md` |
| `autolink` | `create`, `read_one`, `delete` | 4 | `plan/components/autolink.md` |
| `base-gist` | `create` | 1 | `plan/components/base-gist.md` |
| `blob` | `read_one` | 1 | `plan/components/blob.md` |
| `branch-protection` | `read_one` | 1 | `plan/components/branch-protection.md` |
| `branch-restriction-policy` | `read_one` | 1 | `plan/components/branch-restriction-policy.md` |
| `branch-with-protection` | `create`, `read_one` | 2 | `plan/components/branch-with-protection.md` |
| `check-automated-security-fixes` | `read_one` | 1 | `plan/components/check-automated-security-fixes.md` |
| `check-run` | `create`, `read_one`, `update_partial` | 5 | `plan/components/check-run.md` |
| `check-suite` | `create`, `read_one` | 3 | `plan/components/check-suite.md` |
| `check-suite-preference` | `update_partial` | 1 | `plan/components/check-suite-preference.md` |
| `classroom` | `read_one`, `read_many` | 2 | `plan/components/classroom.md` |
| `classroom-assignment` | `read_one` | 1 | `plan/components/classroom-assignment.md` |
| `clone-traffic` | `read_one` | 1 | `plan/components/clone-traffic.md` |
| `code-frequency-stat` | `read_many` | 1 | `plan/components/code-frequency-stat.md` |
| `code-of-conduct` | `read_one` | 1 | `plan/components/code-of-conduct.md` |
| `code-scanning-alert` | `read_one`, `update_partial` | 2 | `plan/components/code-scanning-alert.md` |
| `code-scanning-analysis` | `read_one` | 1 | `plan/components/code-scanning-analysis.md` |
| `code-scanning-analysis-deletion` | `delete` | 1 | `plan/components/code-scanning-analysis-deletion.md` |
| `code-scanning-codeql-database` | `read_one` | 1 | `plan/components/code-scanning-codeql-database.md` |
| `code-scanning-default-setup` | `read_one` | 1 | `plan/components/code-scanning-default-setup.md` |
| `code-scanning-default-setup-update` | `update_partial` | 1 | `plan/components/code-scanning-default-setup-update.md` |
| `code-scanning-sarifs-receipt` | `create` | 1 | `plan/components/code-scanning-sarifs-receipt.md` |
| `code-scanning-sarifs-status` | `read_one` | 1 | `plan/components/code-scanning-sarifs-status.md` |
| `code-scanning-variant-analysis` | `create`, `read_one` | 2 | `plan/components/code-scanning-variant-analysis.md` |
| `code-scanning-variant-analysis-repo-task` | `read_one` | 1 | `plan/components/code-scanning-variant-analysis-repo-task.md` |
| `code-security-configuration` | `create`, `read_one`, `update_partial` | 3 | `plan/components/code-security-configuration.md` |
| `code-security-configuration-for-repository` | `read_one` | 1 | `plan/components/code-security-configuration-for-repository.md` |
| `code-security-default-configurations` | `read_one` | 1 | `plan/components/code-security-default-configurations.md` |
| `codespace` | `create`, `read_one`, `read_many`, `update_partial`, `delete` | 14 | `plan/components/codespace.md` |
| `codespace-export-details` | `create`, `read_one` | 2 | `plan/components/codespace-export-details.md` |
| `codespace-with-full-repository` | `create` | 1 | `plan/components/codespace-with-full-repository.md` |
| `codespaces-org-secret` | `read_one` | 1 | `plan/components/codespaces-org-secret.md` |
| `codespaces-permissions-check-for-devcontainer` | `read_one` | 1 | `plan/components/codespaces-permissions-check-for-devcontainer.md` |
| `codespaces-public-key` | `read_one` | 2 | `plan/components/codespaces-public-key.md` |
| `codespaces-secret` | `read_one` | 1 | `plan/components/codespaces-secret.md` |
| `codespaces-user-public-key` | `read_many` | 1 | `plan/components/codespaces-user-public-key.md` |
| `collaborator` | `read_one`, `update`, `delete` | 6 | `plan/components/collaborator.md` |
| `combined-billing-usage` | `read_one` | 2 | `plan/components/combined-billing-usage.md` |
| `combined-commit-status` | `read_one` | 1 | `plan/components/combined-commit-status.md` |
| `commit` | `create`, `read_one`, `read_many` | 6 | `plan/components/commit.md` |
| `commit-comment` | `create`, `read_one`, `update_partial` | 3 | `plan/components/commit-comment.md` |
| `commit-comparison` | `read_one` | 1 | `plan/components/commit-comparison.md` |
| `community-profile` | `read_one` | 1 | `plan/components/community-profile.md` |
| `content-file` | `read_one` | 2 | `plan/components/content-file.md` |
| `content-tree` | `read_one` | 1 | `plan/components/content-tree.md` |
| `contributor` | `read_one` | 2 | `plan/components/contributor.md` |
| `copilot-organization-details` | `read_one` | 1 | `plan/components/copilot-organization-details.md` |
| `copilot-seat-details` | `read_one` | 1 | `plan/components/copilot-seat-details.md` |
| `custom-property` | `read_one`, `update` | 2 | `plan/components/custom-property.md` |
| `dependabot-alert` | `read_one`, `update_partial` | 2 | `plan/components/dependabot-alert.md` |
| `dependabot-public-key` | `read_one` | 2 | `plan/components/dependabot-public-key.md` |
| `dependabot-secret` | `read_one` | 1 | `plan/components/dependabot-secret.md` |
| `dependency-graph-diff` | `read_one` | 1 | `plan/components/dependency-graph-diff.md` |
| `dependency-graph-spdx-sbom` | `read_one` | 1 | `plan/components/dependency-graph-spdx-sbom.md` |
| `deploy-key` | `create`, `read_one` | 2 | `plan/components/deploy-key.md` |
| `deployment` | `create`, `read_one`, `delete` | 4 | `plan/components/deployment.md` |
| `deployment-branch-policy` | `read_one`, `delete` | 3 | `plan/components/deployment-branch-policy.md` |
| `deployment-branch-policy-name-pattern` | `update` | 1 | `plan/components/deployment-branch-policy-name-pattern.md` |
| `deployment-branch-policy-name-pattern-with-type` | `create` | 1 | `plan/components/deployment-branch-policy-name-pattern-with-type.md` |
| `deployment-protection-rule` | `create`, `read_one` | 2 | `plan/components/deployment-protection-rule.md` |
| `deployment-status` | `create`, `read_one` | 2 | `plan/components/deployment-status.md` |
| `discussion` | `read_one`, `delete` | 4 | `plan/components/discussion.md` |
| `email` | `create`, `read_many`, `delete` | 3 | `plan/components/email.md` |
| `empty-object` | `create`, `read_one`, `update` | 21 | `plan/components/empty-object.md` |
| `enabled-repositories` | `update` | 1 | `plan/components/enabled-repositories.md` |
| `environment` | `read_one`, `update`, `delete` | 4 | `plan/components/environment.md` |
| `event` | `read_one`, `read_many` | 7 | `plan/components/event.md` |
| `feed` | `read_many` | 1 | `plan/components/feed.md` |
| `file-commit` | `update`, `delete` | 2 | `plan/components/file-commit.md` |
| `full-repository` | `create`, `read_one`, `update_partial` | 7 | `plan/components/full-repository.md` |
| `gist-comment` | `create`, `read_one`, `update_partial` | 3 | `plan/components/gist-comment.md` |
| `gist-simple` | `create`, `read_one`, `update_partial` | 4 | `plan/components/gist-simple.md` |
| `git-commit` | `create`, `read_one` | 2 | `plan/components/git-commit.md` |
| `git-ref` | `create`, `read_one`, `update_partial` | 3 | `plan/components/git-ref.md` |
| `git-tag` | `create`, `read_one` | 2 | `plan/components/git-tag.md` |
| `git-tree` | `create`, `read_one` | 2 | `plan/components/git-tree.md` |
| `gitignore-template` | `read_one` | 1 | `plan/components/gitignore-template.md` |
| `global-advisory` | `read_one` | 1 | `plan/components/global-advisory.md` |
| `gpg-key` | `create`, `read_one` | 2 | `plan/components/gpg-key.md` |
| `hook` | `create`, `read_one`, `update_partial`, `delete` | 7 | `plan/components/hook.md` |
| `hook-delivery` | `read_one` | 3 | `plan/components/hook-delivery.md` |
| `hovercard` | `read_one` | 1 | `plan/components/hovercard.md` |
| `import` | `read_one`, `update`, `update_partial`, `delete` | 5 | `plan/components/import.md` |
| `installation` | `read_one`, `read_many`, `delete` | 8 | `plan/components/installation.md` |
| `installation-token` | `create` | 1 | `plan/components/installation-token.md` |
| `integration` | `read_one`, `read_many` | 2 | `plan/components/integration.md` |
| `interaction-limit` | `read_one`, `read_many`, `update`, `delete` | 9 | `plan/components/interaction-limit.md` |
| `issue` | `create`, `read_one`, `read_many`, `update_partial`, `delete` | 10 | `plan/components/issue.md` |
| `issue-comment` | `create`, `read_one`, `update_partial` | 3 | `plan/components/issue-comment.md` |
| `issue-event` | `read_one` | 1 | `plan/components/issue-event.md` |
| `job` | `read_one` | 3 | `plan/components/job.md` |
| `key` | `create`, `read_one`, `read_many`, `delete` | 7 | `plan/components/key.md` |
| `label` | `create`, `read_one`, `read_many`, `update`, `update_partial`, `delete` | 22 | `plan/components/label.md` |
| `language` | `read_one` | 1 | `plan/components/language.md` |
| `license` | `read_one` | 1 | `plan/components/license.md` |
| `license-content` | `read_one` | 1 | `plan/components/license-content.md` |
| `locked-issue-event` | `update`, `delete` | 4 | `plan/components/locked-issue-event.md` |
| `marketplace-purchase` | `read_one` | 2 | `plan/components/marketplace-purchase.md` |
| `merged-upstream` | `create`, `read_one` | 2 | `plan/components/merged-upstream.md` |
| `migration` | `create`, `read_one`, `read_many` | 6 | `plan/components/migration.md` |
| `milestone` | `create`, `read_one`, `update_partial`, `delete` | 5 | `plan/components/milestone.md` |
| `minimal-repository` | `create` | 1 | `plan/components/minimal-repository.md` |
| `oidc-custom-sub` | `read_one`, `update` | 2 | `plan/components/oidc-custom-sub.md` |
| `oidc-custom-sub-repo` | `read_one` | 1 | `plan/components/oidc-custom-sub-repo.md` |
| `org-hook` | `create`, `read_one`, `update_partial` | 3 | `plan/components/org-hook.md` |
| `org-membership` | `read_one`, `update`, `update_partial` | 4 | `plan/components/org-membership.md` |
| `organization-actions-secret` | `read_one` | 1 | `plan/components/organization-actions-secret.md` |
| `organization-actions-variable` | `read_one` | 1 | `plan/components/organization-actions-variable.md` |
| `organization-dependabot-secret` | `read_one` | 1 | `plan/components/organization-dependabot-secret.md` |
| `organization-full` | `read_one`, `update_partial` | 2 | `plan/components/organization-full.md` |
| `organization-invitation` | `create` | 1 | `plan/components/organization-invitation.md` |
| `organization-role` | `read_one` | 2 | `plan/components/organization-role.md` |
| `package` | `read_one`, `read_many`, `delete` | 9 | `plan/components/package.md` |
| `package-version` | `read_one` | 3 | `plan/components/package-version.md` |
| `packages-billing-usage` | `read_one` | 2 | `plan/components/packages-billing-usage.md` |
| `page` | `create`, `read_one`, `update`, `delete` | 4 | `plan/components/page.md` |
| `page-build` | `read_one` | 2 | `plan/components/page-build.md` |
| `page-build-status` | `create` | 1 | `plan/components/page-build-status.md` |
| `page-deployment` | `create` | 1 | `plan/components/page-deployment.md` |
| `pages-deployment-status` | `read_one` | 1 | `plan/components/pages-deployment-status.md` |
| `pages-health-check` | `read_one` | 1 | `plan/components/pages-health-check.md` |
| `participation-stats` | `read_one` | 1 | `plan/components/participation-stats.md` |
| `personal-access-token-request` | `create`, `read_one` | 3 | `plan/components/personal-access-token-request.md` |
| `porter-author` | `update_partial` | 1 | `plan/components/porter-author.md` |
| `private-user` | `update_partial` | 1 | `plan/components/private-user.md` |
| `private-vulnerability-report-create` | `create` | 1 | `plan/components/private-vulnerability-report-create.md` |
| `project` | `create`, `read_one`, `update`, `update_partial`, `delete` | 15 | `plan/components/project.md` |
| `project-card` | `create`, `read_one`, `update_partial` | 3 | `plan/components/project-card.md` |
| `project-collaborator-permission` | `read_one` | 1 | `plan/components/project-collaborator-permission.md` |
| `project-column` | `create`, `read_one`, `update_partial` | 3 | `plan/components/project-column.md` |
| `protected-branch` | `update` | 1 | `plan/components/protected-branch.md` |
| `protected-branch-admin-enforced` | `create`, `read_one` | 4 | `plan/components/protected-branch-admin-enforced.md` |
| `protected-branch-pull-request-review` | `read_one`, `update_partial` | 2 | `plan/components/protected-branch-pull-request-review.md` |
| `public-user` | `read_one`, `read_many` | 3 | `plan/components/public-user.md` |
| `pull-request` | `create`, `read_one`, `update_partial` | 3 | `plan/components/pull-request.md` |
| `pull-request-merge-result` | `update` | 1 | `plan/components/pull-request-merge-result.md` |
| `pull-request-review` | `create`, `read_one`, `update`, `delete` | 6 | `plan/components/pull-request-review.md` |
| `pull-request-review-comment` | `create`, `read_one`, `update_partial` | 4 | `plan/components/pull-request-review-comment.md` |
| `pull-request-review-request` | `read_one` | 1 | `plan/components/pull-request-review-request.md` |
| `pull-request-simple` | `create`, `delete` | 2 | `plan/components/pull-request-simple.md` |
| `rate-limit-overview` | `read_many` | 1 | `plan/components/rate-limit-overview.md` |
| `reaction` | `create`, `read_one`, `delete` | 25 | `plan/components/reaction.md` |
| `release` | `create`, `read_one`, `update_partial` | 5 | `plan/components/release.md` |
| `release-asset` | `create`, `read_one`, `update_partial` | 3 | `plan/components/release-asset.md` |
| `release-notes-content` | `create` | 1 | `plan/components/release-notes-content.md` |
| `repo-codespaces-secret` | `read_one` | 1 | `plan/components/repo-codespaces-secret.md` |
| `repository` | `read_one`, `read_many`, `update`, `delete` | 45 | `plan/components/repository.md` |
| `repository-advisory` | `read_one` | 1 | `plan/components/repository-advisory.md` |
| `repository-advisory-create` | `create` | 1 | `plan/components/repository-advisory-create.md` |
| `repository-advisory-update` | `update_partial` | 1 | `plan/components/repository-advisory-update.md` |
| `repository-collaborator-permission` | `read_one` | 1 | `plan/components/repository-collaborator-permission.md` |
| `repository-invitation` | `update`, `update_partial` | 2 | `plan/components/repository-invitation.md` |
| `repository-ruleset` | `create`, `read_one`, `update` | 6 | `plan/components/repository-ruleset.md` |
| `repository-subscription` | `read_one`, `update` | 2 | `plan/components/repository-subscription.md` |
| `root` | `read_many` | 1 | `plan/components/root.md` |
| `rule-suite` | `read_one` | 2 | `plan/components/rule-suite.md` |
| `rule-suites` | `read_one` | 2 | `plan/components/rule-suites.md` |
| `runner` | `read_one`, `delete` | 6 | `plan/components/runner.md` |
| `secret-scanning-alert` | `read_one`, `update_partial` | 2 | `plan/components/secret-scanning-alert.md` |
| `secret-scanning-push-protection-bypass` | `create` | 1 | `plan/components/secret-scanning-push-protection-bypass.md` |
| `selected-actions` | `read_one`, `update` | 4 | `plan/components/selected-actions.md` |
| `short-blob` | `create` | 1 | `plan/components/short-blob.md` |
| `snapshot` | `create` | 1 | `plan/components/snapshot.md` |
| `ssh-signing-key` | `create`, `read_one` | 2 | `plan/components/ssh-signing-key.md` |
| `stargazer` | `read_one`, `update`, `delete` | 4 | `plan/components/stargazer.md` |
| `starred-repository` | `read_one`, `read_many`, `update`, `delete` | 6 | `plan/components/starred-repository.md` |
| `status` | `create`, `read_one` | 3 | `plan/components/status.md` |
| `status-check-policy` | `read_one`, `update_partial` | 2 | `plan/components/status-check-policy.md` |
| `tag` | `read_one` | 1 | `plan/components/tag.md` |
| `tag-protection` | `create` | 1 | `plan/components/tag-protection.md` |
| `team` | `create`, `read_one`, `read_many`, `update`, `delete` | 18 | `plan/components/team.md` |
| `team-discussion` | `create`, `read_one`, `update_partial` | 6 | `plan/components/team-discussion.md` |
| `team-discussion-comment` | `create`, `read_one`, `update_partial` | 6 | `plan/components/team-discussion-comment.md` |
| `team-full` | `create`, `read_one`, `update_partial` | 5 | `plan/components/team-full.md` |
| `team-membership` | `read_one`, `update` | 4 | `plan/components/team-membership.md` |
| `team-project` | `read_one` | 2 | `plan/components/team-project.md` |
| `team-repository` | `read_one` | 2 | `plan/components/team-repository.md` |
| `thread` | `read_one`, `update_partial`, `delete` | 3 | `plan/components/thread.md` |
| `thread-subscription` | `read_one`, `update` | 2 | `plan/components/thread-subscription.md` |
| `timeline-assigned-issue-event` | `read_one` | 1 | `plan/components/timeline-assigned-issue-event.md` |
| `topic` | `read_one`, `read_many`, `update` | 3 | `plan/components/topic.md` |
| `user-marketplace-purchase` | `read_one`, `read_many` | 2 | `plan/components/user-marketplace-purchase.md` |
| `view-traffic` | `read_one` | 1 | `plan/components/view-traffic.md` |
| `webhook-config` | `read_one`, `read_many`, `update_partial` | 6 | `plan/components/webhook-config.md` |
| `workflow` | `read_one` | 2 | `plan/components/workflow.md` |
| `workflow-run` | `read_one` | 2 | `plan/components/workflow-run.md` |
| `workflow-run-usage` | `read_one` | 1 | `plan/components/workflow-run-usage.md` |
| `workflow-usage` | `read_one` | 1 | `plan/components/workflow-usage.md` |

## Quick Stats

**Operations by Type:**
- `create`: 116 routes
- `read_one`: 292 routes
- `read_many`: 33 routes
- `update`: 65 routes
- `update_partial`: 47 routes
- `delete`: 73 routes

**Routes by Status:**
- `needs_mapping`: 326 routes
- `planned`: 626 routes

---

**Note:** For detailed route-by-route information, see individual component plan files in `plan/components/`.
