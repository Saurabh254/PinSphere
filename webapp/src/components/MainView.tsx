import api_client from "@/api_client";
import { API_URL } from "@/constants";
import { Content, Page } from "@/types";
import { Axios } from "axios";
import { useEffect, useState } from "react";
import ContentWithBlurhash from "./ContentWithBlurhash";
import CardsShimmer from "./shimmer/CardsShimmer";

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
  if (contents === null) {
    return <CardsShimmer />;
  }
  return (
    <div className="columns-2 gap-x-2 bg-background lg:columns-4 space-y-2  px-2 pt-2 text-light ">
      {contents &&
        contents.items.map((content) => (
          <ContentWithBlurhash content={content} key={content.id} />
        ))}
    </div>
  );
};

export default MainView;
