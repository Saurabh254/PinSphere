from typing import List, Literal, Optional

import pytz
from pydantic import BaseModel, Field


# ---------- Nested Setting Models ----------
class GeneralSettingsFilter(BaseModel):
    language: Optional[str] = Field(
        default=None, description="Language code like 'en', 'fr'."
    )
    timezone: Optional[str] = Field(
        default=None, description="Timezone like 'Asia/Kolkata'."
    )
    background_sync: Optional[bool] = Field(
        default=None, description="Enable background sync."
    )
    autoplay_media: Optional[bool] = Field(
        default=None, description="Autoplay media setting."
    )

    @classmethod
    def validate_timezone(cls, value: Optional[str]) -> Optional[str]:
        if value and value not in pytz.all_timezones:
            raise ValueError(f"Invalid timezone: {value}")
        return value

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_timezone


class NotificationSettingsFilter(BaseModel):
    updates_notification: Optional[bool] = Field(
        default=None, description="Receive update notifications."
    )
    mail_updates: Optional[bool] = Field(
        default=None, description="Receive mail update notifications."
    )
    incoming_sound: Optional[bool] = Field(
        default=None, description="Enable incoming sound notifications."
    )


class AppearanceSettingsFilter(BaseModel):
    accent_colors: Optional[List[str]] = Field(
        default=None,
        description="List of selected accent colors (e.g. ['blue', 'purple']).",
    )


class PrivacySecuritySettingsFilter(BaseModel):
    private_account: Optional[bool] = Field(
        default=None, description="Enable private account."
    )
    two_factor_auth: Optional[bool] = Field(
        default=None, description="Enable two-factor authentication."
    )
    read_receipts: Optional[bool] = Field(
        default=None, description="Allow read receipts."
    )
    profile_discovery: Optional[bool] = Field(
        default=None, description="Allow others to find your profile."
    )


# ---------- Main Filter Wrapper ----------
class SettingsFilter(BaseModel):
    settings_type: Literal[
        "general", "notification", "appearance", "privacy_and_security"
    ]

    general: Optional[GeneralSettingsFilter] = None
    notification: Optional[NotificationSettingsFilter] = None
    appearance: Optional[AppearanceSettingsFilter] = None
    privacy_and_security: Optional[PrivacySecuritySettingsFilter] = None
