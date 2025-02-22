import { FileContentType } from "../types";
import axios from "axios";

export function isValidContentType(value: string): boolean {
  return Object.values(FileContentType).includes(value as FileContentType);
}

type PreSignedUrlType = {
  url: string;
  fields: {
    [key: string]: string;
  };
};

export const upload_file = async (data: PreSignedUrlType, file: File) => {
  const formdata = new FormData();

  // Ensure fields (key, policy, etc.) come before the file
  Object.entries(data.fields).forEach(([key, val]) => {
    formdata.append(key, val);
  });
  formdata.append("Content-Type", file.type);

  // Append the file correctly (no need for "image.png" as the third argument)
  formdata.append("file", file);
  const uninterceptedAxiosInstance = axios.create();
  return await uninterceptedAxiosInstance.post(data.url, formdata, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};
