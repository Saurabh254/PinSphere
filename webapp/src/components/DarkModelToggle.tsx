import { RiContrast2Line, RiSunLine } from "@remixicon/react";

const DarkModelToggle = () => {
  return (
    <div>
      <RiContrast2Line aria-label="enabled" />

      <RiSunLine
        aria-label="disabled"
        className="rounded-full border-none p-1 outline-none "
      />
    </div>
  );
};

export default DarkModelToggle;
