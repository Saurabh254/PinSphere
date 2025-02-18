import { Content, FileContentType } from "../types";
import ImageWithBlurhash from "./ImageWithBlurhash";
interface ContentWithBlurhashProps {
  content: Content;
}
import ReactAudioPlayer from "react-audio-player";

const ContentWithBlurhash = ({ content }: ContentWithBlurhashProps) => {
  console.log(content.metadata);
  if (
    (content.metadata.content_type &&
      content.metadata.content_type == FileContentType.JPEG) ||
    content.metadata.content_type == FileContentType.PNG ||
    content.metadata.content_type == FileContentType.GIF
  ) {
    return <ImageWithBlurhash image={content} key={content.id} />;
  } else if (
    content.metadata.content_type == FileContentType.MP3 ||
    content.metadata.content_type == FileContentType.WAV ||
    content.metadata.content_type == FileContentType.OGG
  ) {
    return <ReactAudioPlayer src={content.url} controls />;
  } else {
    return <video src={content.url} controls className="rounded-lg" />;
  }
};
export default ContentWithBlurhash;
