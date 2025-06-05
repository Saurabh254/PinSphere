import { RiHomeSmileLine, RiNotificationLine } from "@remixicon/react";
import { Lock } from "lucide-react";

const SettingsMenu: React.FC<{
  settingsType: number;
  setSettingsType: React.Dispatch<React.SetStateAction<number>>;
}> = ({ settingsType, setSettingsType }) => {
  return (
    <ul className="menu menu-horizontal  w-full flex  justify-evenly   border-b-2 border-gray-700 pb-2 mb-6">
      <li>
        <a
          className={` ${
            settingsType === 0 ? "dark:bg-gray-700 bg-gray-300" : ""
          }`}
          data-tip="Home"
          onClick={() => setSettingsType(0)}
        >
          <RiHomeSmileLine />
        </a>
      </li>
      <li>
        <a
          className={` ${
            settingsType === 1 ? "dark:bg-gray-700 bg-gray-300" : ""
          }`}
          data-tip="Notification"
          onClick={() => setSettingsType(1)}
        >
          <RiNotificationLine />
        </a>
      </li>

      <li>
        <a
          className={` ${
            settingsType === 2 ? "dark:bg-gray-700 bg-gray-300" : ""
          }`}
          data-tip="Privacy & Security"
          onClick={() => setSettingsType(2)}
        >
          <Lock />
        </a>
      </li>
    </ul>
  );
};

export default SettingsMenu;
