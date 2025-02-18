import { FileContentType } from "../types";

export function isValidContentType(value: string): boolean {
    return Object.values(FileContentType).includes(value as FileContentType);
}