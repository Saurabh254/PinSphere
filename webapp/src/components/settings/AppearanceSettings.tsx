import { Moon, Sun } from "lucide-react";
import React, { useState, useEffect } from "react";

const themes = [
  "light",
  "dark",
  "cupcake",
  "bumblebee",
  "emerald",
  "corporate",
];
const accentColors = [
  "#3b82f6",
  "#f59e0b",
  "#10b981",
  "#ef4444",
  "#8b5cf6",
  "#ec4899",
];

const AppearanceSettings: React.FC = () => {
  return (
    <div className="p-0 px-6 space-y-6">
      <h2 className="text-lg dark:text-gray-200 font-semibold">
        Appearance Settings
      </h2>

      {/* Accent Color Picker */}
      <div>
        <label className="label font-medium">Accent Color</label>
        <div className="flex gap-3 flex-wrap mt-4 w-full justify-evenly">
          {accentColors.map((color) => (
            <button
              key={color}
              className={`w-8 h-8 rounded-full border-2 transition-all ${
                color === "dark"
                  ? "ring ring-offset-2 ring-primary"
                  : "border-gray-300"
              }`}
              style={{ backgroundColor: color }}
              onClick={() => {}}
            ></button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AppearanceSettings;
