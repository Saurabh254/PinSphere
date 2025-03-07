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
export interface Content {
  id: string;
  url: string;
  blurhash: string;
  username: string;
  description: string;
  likes: number;
  user: User
  metadata: Metadata;
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
