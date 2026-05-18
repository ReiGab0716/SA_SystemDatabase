# Website System Bug Fix Checklist

## Issues Reported
- [x] Add uploadable service photos in Django admin/service management.
- [x] Show the correct registration restriction message when registration cannot continue.
- [x] Auto-scroll after an existing patient is selected in staff Schedule Appointment.
- [x] Fix uploaded patient/profile photos not showing, including in staff patient information views.

## Implementation Checklist
- [x] Add a `Service.image` upload field and admin preview.
- [x] Render uploaded service images on the public services section with static fallback images.
- [x] Improve registration template error/message display and preserve entered values after validation errors.
- [x] Scroll the selected patient panel into view after staff choose an existing patient.
- [x] Include profile image URLs in patient detail API responses.
- [x] Show patient photos in doctor/secretary patient information modals and patient detail page.
- [x] Serve uploaded media URLs in deployed environments.
- [x] Run Django validation and create migrations.
- [x] Ensure Render runs database migrations before starting the web server.
- [x] Commit and push changes to GitHub for Render auto-deploy.
