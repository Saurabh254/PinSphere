import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";

interface PasswordInputProps {
  formData: { password: string };
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const PasswordInput: React.FC<PasswordInputProps> = ({
  formData,
  handleChange,
}) => {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="relative w-full">
      <input
        type={showPassword ? "text" : "password"}
        id="password"
        value={formData.password}
        onChange={handleChange}
        placeholder="Enter your password"
        className="w-full bg-input dark:text-primary-content text-primary text-sm placeholder:text-foreground autofill:text-primary ring-primary ring-1 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-color-secondary"
      />
      <button
        type="button"
        className="absolute inset-y-0 right-3 flex items-center text-gray-500"
        onClick={() => setShowPassword(!showPassword)}
      >
        {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
      </button>
    </div>
  );
};

export default PasswordInput;
