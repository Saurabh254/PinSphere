export type GeneralSettings = {
    language: string;
    timezone: string;
    background_sync: boolean;
    autoplay_media: boolean;
};
export type NotificationSettings = {
    updates_notification: boolean;
    mail_updates: boolean;
    incoming_sound: boolean;
};

export type AppearanceSettings = {
    theme: string;

}

export type PrivacyAndSecurity = {
    private_account: boolean;
    two_factor_auth: boolean;
    read_receipts: boolean;
    profile_discovery: boolean;
}
export type UserSettings = {
    general: GeneralSettings
    notification: NotificationSettings
    privacy_and_security: PrivacyAndSecurity
}