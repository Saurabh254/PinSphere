interface Metadata {
  height: number;
  width: number;
}

export interface Image {
  id: string;
  url: string;
  blurhash: string;
  description: string;
  metadata: Metadata;
}
