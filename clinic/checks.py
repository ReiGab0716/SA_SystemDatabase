from pathlib import Path

from django.conf import settings
from django.core.checks import Warning, register


@register(deploy=True)
def media_storage_check(app_configs, **kwargs):
    """Warn when production uploads are stored in the app's temporary folder."""
    media_root = Path(settings.MEDIA_ROOT).resolve()
    default_media_root = (settings.BASE_DIR / "media").resolve()

    if media_root != default_media_root:
        return []

    return [
        Warning(
            "Uploaded media is using the default project media folder.",
            hint=(
                "Set MEDIA_ROOT to a persistent disk path such as "
                "/var/data/media on Render. Otherwise uploaded patient and "
                "service photos can disappear after restarts, redeploys, or "
                "sleep/wake cycles."
            ),
            id="clinic.W001",
        )
    ]
