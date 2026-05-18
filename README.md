# Shields Aesthetics
Appointment Setting, Time Restrictions, 1 to 1 Appointment.

## Uploaded photos in deployment

Patient profile photos and uploaded service photos are stored under
`MEDIA_ROOT`. In production, set `MEDIA_ROOT` to persistent storage. For
Render, create a persistent disk mounted at `/var/data` and set:

```env
MEDIA_ROOT=/var/data/media
```

If production uses the default project `media/` folder, uploaded files can be
lost after restarts, redeploys, or sleep/wake cycles even though the database
still contains the saved photo path.
