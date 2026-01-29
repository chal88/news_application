# Use Case Diagram – Django News Application

## Actors
- Reader
- Journalist
- Editor

## Use Cases and Relationships

Reader ─────────────▶ View Approved Articles
Reader ─────────────▶ Read Full Article
Reader ─────────────▶ Receive Email Notifications

Journalist ─────────▶ Register Account
Journalist ─────────▶ Login
Journalist ─────────▶ Submit Article
Journalist ─────────▶ Edit Own Article

Editor ─────────────▶ Login
Editor ─────────────▶ View Pending Articles
Editor ─────────────▶ Approve Article
Editor ─────────────▶ Update
Editor ─────────────▶ Delete

Approve Article ────▶ Trigger Notifications

## Unit Test Coverage Mapping

- User Registration → UserRegistrationTest
- Role Assignment → UserRoleAssignmentTest
- Article Submission → ArticleWorkflowTest
- Article Approval → ArticleWorkflowTest

