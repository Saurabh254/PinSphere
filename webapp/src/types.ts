interface Metadata {
  height: number;
  width: number;
  content_type: FileContentType;
}

export interface User {

  username: string,
  name: string,
  email: string,
  bio: string | null,
  created_at: Date,
  url: string | null,
}

export interface SlimContent {
  id: string;
  url: string;
  blurhash: string;
  user_id: string;
  description: string;
  likes: number;
  metadata: Metadata;

}
export interface Content extends SlimContent {
  user: User
}

export type Page<T> = {
  items: T[];
  pages: number;
  page: number;
  total: number;
  size: number;

}

export enum FileContentType {
  JPEG = "image/jpeg",
  PNG = "image/png",
  GIF = "image/gif",
  MP4 = "video/mp4",
  WEBM = "video/webm",
  MP3 = "audio/mpeg",
  WAV = "audio/wav",
  OGG = "audio/ogg",
}
