import { useState } from "react";

const NotificationSettings = () => {
  const [settings, setSettings] = useState({
    messageNotifications: false,
    showPreviews: false,
    showReactionNotifications: false,
    backgroundSync: false,
    incomingSounds: true,
    outgoingSounds: false,
  });

  const toggleSetting = (key: keyof typeof settings) => {
    setSettings((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  return (
    <div className="p-6 pt-0 max-w-md  text-sm dark:text-gray-200 space-y-5">
      <div>
        <h2 className="text-lg font-semibold">Notifications and Sounds</h2>
      </div>

      {/* Message Notifications */}
      <div className="flex items-center justify-between">
        <div>
          <div className="font-medium">Updates notifications</div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Show notifications for new updates
          </p>
        </div>
        <input
          type="checkbox"
          className="toggle toggle-primary bg-black"
          checked={settings.messageNotifications}
          onChange={() => toggleSetting("messageNotifications")}
        />
      </div>

      {/* Email updates*/}
      <div className="flex items-center justify-between">
        <div>
          <div className="font-medium">Mail Updates</div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Send updates on registered mail
          </p>
        </div>
        <input
          type="checkbox"
          className="toggle  toggle-primary bg-black"
          checked={settings.outgoingSounds}
          onChange={() => toggleSetting("outgoingSounds")}
        />
      </div>
      {/* Incoming Sounds */}
      <div className="flex items-center justify-between">
        <div>
          <div className="font-medium">Incoming sounds</div>
          <p className="text-xs text-gray-500  dark:text-gray-400">
            Play sounds for incoming messages
          </p>
        </div>
        <input
          type="checkbox"
          className="toggle  toggle-primary bg-black"
          checked={settings.incomingSounds}
          onChange={() => toggleSetting("incomingSounds")}
        />
      </div>

      {/* Outgoing Sounds */}
      <div className="flex items-center justify-between">
        <div>
          <div className="font-medium">AutoPlay Media</div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Play media automatically
          </p>
        </div>
        <input
          type="checkbox"
          className="toggle  toggle-primary bg-black"
          checked={settings.showPreviews}
          onChange={() => toggleSetting("showPreviews")}
        />
      </div>
    </div>
  );
};

export default NotificationSettings;
