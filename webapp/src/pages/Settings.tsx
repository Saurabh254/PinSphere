import GeneralSettings from "@/components/settings/GeneralSettings";
import NotificationSettings from "@/components/settings/NotificationSettings";
import PrivacyAndSecuritySettings from "@/components/settings/PrivacyAndSettings";
import SettingsMenu from "@/components/SettingsMenu";
import { getUserSettings } from "@/service/user_service";
import { UserSettings } from "@/types/userSettings";
import { useEffect, useState } from "react";

import React from "react";

const SettingsContent: React.FC<{
  settingsType: number;
}> = ({ settingsType }) => {
  const [userSettings, setUserSettings] = useState<UserSettings | null>(null);
  useEffect(() => {
    const call_api = async () => {
      try {
        setUserSettings(await getUserSettings());
      } catch (e) {
        console.error(e);
      }
    };
    call_api();
  }, []);
  if (userSettings === null) {
    return <h1>loadingg....</h1>;
  }
  switch (settingsType) {
    case 0:
      return <GeneralSettings generalSettings={userSettings.general} />;
    case 1:
      return <NotificationSettings />;
    case 2:
      return <PrivacyAndSecuritySettings />;
  }

  return <div className="main">page not found</div>;
};

const Settings = () => {
  const [settingsType, setSettingsType] = useState<number>(0);
  return (
    <main>
      <SettingsMenu
        settingsType={settingsType}
        setSettingsType={setSettingsType}
      />
      <SettingsContent settingsType={settingsType} />
    </main>
  );
};
export default Settings;
