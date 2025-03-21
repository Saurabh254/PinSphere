import api_client from "@/api_client";
import { API_URL } from "@/constants";
import { Content, Page } from "@/types";
import { Axios } from "axios";
import { useEffect, useState } from "react";
import ContentWithBlurhash from "./ContentWithBlurhash";

const MainView = () => {
  const [contents, setContents] = useState<Page<Content> | null>(null);

  useEffect(() => {
    const api_call = async () => {
      await api_client
        .get(API_URL + "/content")
        .then((result) => {
          setContents(result.data);
        })
        .catch((err: Axios) => {
          console.log(err);
        });
    };
    api_call();
  }, []);

  return (
    // <div className="grid grid-cols-2 md:grid-cols-3 [&>*]:h-auto w-full h-full overflow-scroll gap-4 space-y-4 mt-8  px-4 md:px-8 ">
    <div className="columns-2 gap-x-2 lg:columns-4 space-y-2  px-2 pt-2">
      {contents &&
        contents.items.map((content) => (
          <ContentWithBlurhash content={content} key={content.id} />
        ))}
    </div>
  );
};

export default MainView;
