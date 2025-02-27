import { Content, FileContentType } from "../types";
import ImageWithBlurhash from "./ImageWithBlurhash";
import Audio from "./Audio";
import Pin from "./PinOuter";
interface ContentWithBlurhashProps {
  content: Content;
}

const ContentWithBlurhash = ({ content }: ContentWithBlurhashProps) => {
  if (
    (content.metadata.content_type &&
      content.metadata.content_type == FileContentType.JPEG) ||
    content.metadata.content_type == FileContentType.PNG ||
    content.metadata.content_type == FileContentType.GIF
  ) {
    return (
      <Pin content={content}>
        <ImageWithBlurhash image={content} key={content.id} />{" "}
      </Pin>
    );
  } else if (
    content.metadata.content_type == FileContentType.MP3 ||
    content.metadata.content_type == FileContentType.WAV ||
    content.metadata.content_type == FileContentType.OGG
  ) {
    return (
      <Pin content={content}>
        <Audio content={content} key={content.id} />
      </Pin>
    );
  } else {
    return (
      <Pin content={content}>
        <video src={content.url} controls className="rounded-lg" />
      </Pin>
    );
  }
};
export default ContentWithBlurhash;
