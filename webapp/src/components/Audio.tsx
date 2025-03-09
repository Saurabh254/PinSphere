import React, { useState } from "react";
import ReactAudioPlayer from "react-audio-player";
import { RiPauseFill, RiPlayFill } from "@remixicon/react";
import { SlimContent } from "../types";

interface AudioPlayerProps {
  content: SlimContent;
}

const AudioPlayer = ({ content }: AudioPlayerProps) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = React.useRef<ReactAudioPlayer>(null);

  const togglePlay = () => {
    if (audioRef.current) {
      if (isPlaying) {
        if (audioRef.current.audioEl.current) {
          audioRef.current.audioEl.current.pause();
        }
      } else {
        if (audioRef.current.audioEl.current) {
          audioRef.current.audioEl.current.play();
        }
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div className="flex gap-4 items-center w-full ">
      {/* Audio Player Container */}
      {/* Play/Pause Button */}
      <button
        onClick={togglePlay}
        className="bg-indigo-500 w-48 h-24 rounded-2xl flex items-center justify-center shadow-md hover:bg-indigo-600 transition w-full"
      >
        {isPlaying ? (
          <RiPauseFill className="text-white outline-4 outline-black bg-black rounded-full w-8 h-8" />
        ) : (
          <RiPlayFill className="text-white outline-4 outline-black rounded-full w-8 h-8 bg-black" />
        )}
      </button>
      {/* Hidden Audio Player */}
      <ReactAudioPlayer
        ref={audioRef}
        src={content.url} // Replace with actual audio URL
        controls={false}
      />
    </div>
  );
};

export default AudioPlayer;
