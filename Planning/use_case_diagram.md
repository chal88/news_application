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
Journalist ─────────▶ create and Submit Article
Journalist ─────────▶ Create and Submit Newsletter
Journalist ─────────▶ Edit Own Article

Editor ─────────────▶ Login
Editor ─────────────▶ View Pending Articles
Editor ─────────────▶ Approve Article
Editor ─────────────▶ Update
Editor ─────────────▶ Delete

Admin(Superuser) ─────────▶ Create Editor
Admin(Superuser) ─────────▶ Create Publishing house
Admin(Superuser) ─────────▶ Assign Editor to Publishing House

Approve Article ────▶ Trigger Notifications

## Unit Test Coverage Mapping

- User Registration → UserRegistrationTest
- Role Assignment → UserRoleAssignmentTest
- Article Submission → ArticleWorkflowTest
- Article Approval → ArticleWorkflowTest

