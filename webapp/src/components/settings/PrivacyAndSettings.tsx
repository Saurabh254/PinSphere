import React, { useState } from "react";

const PrivacyAndSecuritySettings = () => {
  const [profileType, setProfileType] = useState(0);
  const [twoFactorAuth, setTwoFactorAuth] = useState(false);
  const [readReceipts, setReadReceipts] = useState(true);
  const [profileDiscovery, setProfileDiscovery] = useState(true);

  return (
    <div className="p-6 pt-0 text-sm ">
      <h2 className="text-lg font-semibold mb-4 text-black dark:text-gray-200">
        Privacy & Security
      </h2>

      {/* Account type selector  */}
      <div className="flex items-center  justify-between gap-4 mb-4">
        <div>
          <span className="block text-black dark:text-gray-200 font-semibold">
            Private Account
          </span>
          <span className="text-xs block text-gray-500">
            if turned on your posts are visible only to approved followers.
            Manage your privacy and control who sees your activity.
          </span>
        </div>
        <input
          type="checkbox"
          className="toggle toggle-primary bg-black"
          checked={profileType !== 0}
          onClick={() => {
            setProfileType(profileType == 0 ? 1 : 0);
          }}
        />
      </div>

      {/* Two Factor Auth */}
      <div className="form-control mb-4">
        <label className="label cursor-pointer justify-between flex">
          <div>
            <span className="label-text font-semibold text-black dark:text-gray-200">
              Two-Factor Authentication
            </span>
            <p className="text-xs text-gray-500 ml-1 mt-1">
              Adds an extra layer of security to your account.
            </p>
          </div>
          <input
            type="checkbox"
            className="toggle  toggle-primary bg-black"
            checked={twoFactorAuth}
            onChange={() => setTwoFactorAuth(!twoFactorAuth)}
          />
        </label>
      </div>

      {/* Read Receipts */}
      <div className="form-control mb-4">
        <label className="label cursor-pointer">
          <div>
            <span className="label-text font-semibold text-black dark:text-gray-200">
              Read Receipts
            </span>
            <p className="text-xs text-gray-500 ml-1 mt-1 text-wrap">
              Allow others to see when you've read their messages.
            </p>
          </div>
          <input
            type="checkbox"
            className="toggle  toggle-primary bg-black"
            checked={readReceipts}
            onChange={() => setReadReceipts(!readReceipts)}
          />
        </label>
      </div>

      {/* Profile Discovery */}
      <div className="form-control mb-4">
        <label className="label cursor-pointer">
          <div>
            <span className="label-text font-semibold text-black dark:text-gray-200">
              Profile Discovery
            </span>
            <p className="text-xs text-gray-500 text-wrap ml-1 mt-1">
              Let others find your profile using your email or username.
            </p>
          </div>
          <input
            type="checkbox"
            className="toggle toggle-primary bg-black"
            checked={profileDiscovery}
            onChange={() => setProfileDiscovery(!profileDiscovery)}
          />
        </label>
      </div>
    </div>
  );
};

export default PrivacyAndSecuritySettings;
