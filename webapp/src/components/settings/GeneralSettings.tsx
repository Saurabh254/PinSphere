import { save_settings } from "@/service/user_service";
import { GeneralSettings as GeneralSettingsType } from "@/types/userSettings";
import { useState } from "react";

const languages = [
  { label: "English", value: "en" },
  { label: "Hindi", value: "hi" },
  { label: "Spanish", value: "es" },
  { label: "French", value: "fr" },
  { label: "German", value: "de" },
  { label: "Chinese", value: "zh" },
];

const timezones = [
  { label: "UTC (Coordinated Universal Time)", value: "UTC" },
  { label: "IST (India Standard Time)", value: "Asia/Kolkata" },
  { label: "EST (Eastern Standard Time)", value: "America/New_York" },
  { label: "PST (Pacific Standard Time)", value: "America/Los_Angeles" },
  { label: "CET (Central European Time)", value: "Europe/Berlin" },
  { label: "JST (Japan Standard Time)", value: "Asia/Tokyo" },
];

const GeneralSettings: React.FC<{ generalSettings: GeneralSettingsType }> = ({
  generalSettings,
}) => {
  const [settings, setSettings] =
    useState<GeneralSettingsType>(generalSettings);
  const [changed, setChanged] = useState<boolean>(false);

  const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setChanged(true);
    setSettings({ ...settings, language: e.target.value });
  };

  const handleTimezoneChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setChanged(true);
    setSettings({ ...settings, timezone: e.target.value });
  };

  const handleBackgroundSyncToggle = () => {
    setChanged(true);
    setSettings({ ...settings, background_sync: !settings.background_sync });
  };

  const handleAutoplayMediaToggle = () => {
    setChanged(true);
    setSettings({ ...settings, autoplay_media: !settings.autoplay_media });
  };

  const handleSave = async () => {
    await save_settings("general", settings);
    setChanged(false);
  };

  return (
    <div className="px-4 py-0 dark:text-gray-200 text-black">
      {changed && (
        <div className="absolute bottom-10 px-4 w-[calc(100%-2rem)] justify-between flex items-center bg-gray-800 rounded-lg py-3">
          <span className="text-sm text-nowrap">You have unsaved changes!</span>
          <button
            type="button"
            className="btn-primary btn btn-sm"
            onClick={handleSave}
          >
            Save
          </button>
        </div>
      )}
      <div className="rounded-xl p-2 py-0 text-sm">
        <h1 className="text-lg font-semibold mb-4">General Settings</h1>

        <div className="space-y-4 text-black dark:text-gray-200">
          {/* Language Selector */}
          <div className="flex flex-col">
            <label htmlFor="language" className="mb-1 font-semibold">
              Language
            </label>
            <select
              id="language"
              name="language"
              value={settings.language}
              onChange={handleLanguageChange}
              className="border-2 border-black font-semibold dark:text-gray-400 px-3 py-2 rounded focus:outline-none focus:ring focus:ring-indigo-500"
            >
              {languages.map((lang) => (
                <option key={lang.value} value={lang.value}>
                  {lang.label}
                </option>
              ))}
            </select>
          </div>

          {/* Timezone Selector */}
          <div className="flex flex-col text-black dark:text-gray-200">
            <label htmlFor="timezone" className="mb-1 font-semibold">
              Timezone
            </label>
            <select
              id="timezone"
              name="timezone"
              value={settings.timezone}
              onChange={handleTimezoneChange}
              className="border-2 border-black dark:text-gray-400 font-semibold px-3 py-2 rounded focus:outline-none focus:ring focus:ring-indigo-500"
            >
              {timezones.map((zone) => (
                <option key={zone.value} value={zone.value}>
                  {zone.label}
                </option>
              ))}
            </select>
          </div>

          {/* Background Sync */}
          <div className="flex items-center justify-between gap-6">
            <div>
              <div className="font-semibold text-black dark:text-gray-200">
                Background sync
              </div>
              <p className="text-xs text-gray-500">
                Get faster performance by syncing messages in the background
              </p>
            </div>
            <input
              type="checkbox"
              className="toggle toggle-primary bg-black"
              checked={settings.background_sync}
              onChange={handleBackgroundSyncToggle}
            />
          </div>

          {/* AutoPlay Media */}
          <div className="flex items-center justify-between gap-6">
            <div>
              <div className="font-semibold text-black dark:text-gray-200">
                AutoPlay Media
              </div>
              <p className="text-xs text-gray-500">
                when checked media will play automatically
              </p>
            </div>
            <input
              type="checkbox"
              className="toggle toggle-primary bg-black"
              checked={settings.autoplay_media}
              onChange={handleAutoplayMediaToggle}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default GeneralSettings;
