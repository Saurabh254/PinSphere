import AppearanceSettings from "@/components/settings/AppearanceSettings";
import GeneralSettings from "@/components/settings/GeneralSettings";
import NotificationSettings from "@/components/settings/NotificationSettings";
import PrivacyAndSecuritySettings from "@/components/settings/PrivacyAndSettings";
import SettingsMenu from "@/components/SettingsMenu";
import { useState } from "react";

import React from "react";

const SettingsContent: React.FC<{
  settingsType: number;
}> = ({ settingsType }) => {
  switch (settingsType) {
    case 0:
      return <GeneralSettings />;
    case 1:
      return <NotificationSettings />;
    case 2:
      return <AppearanceSettings />;
    case 3:
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
