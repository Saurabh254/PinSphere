import React, { useState } from "react";
import {
  RiSearchLine,
  RiImageLine,
  RiFilter3Line,
  RiCloseCircleLine,
} from "@remixicon/react";
import { Content, Page } from "@/types";
import Pin from "@/components/PinOuter";
import ImageWithBlurhash from "@/components/ImageWithBlurhash";
import api_client from "@/api_client";
import { API_URL } from "@/constants";

const ImageContextSearch = () => {
  const [searchText, setSearchText] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [searchedContent, setSearchedContent] = useState<Page<Content> | null>(
    null
  );
  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (searchText.trim()) {
      setIsSearching(true);
      const call_api = async () => {
        try {
          const response = await api_client.get(
            API_URL + `/content/search?text=${searchText}`
          );
          setSearchedContent(response.data);
          setIsSearching(false);
        } catch (e) {
          console.log(e);
        }
      };
      call_api();
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      {/* Search Header */}
      <div className="flex flex-col gap-4">
        {/* Search Form */}
        <form onSubmit={handleSearch} className="flex flex-col gap-4">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <RiSearchLine className="w-5 h-5 text-base-content opacity-70" />
            </div>
            <input
              type="text"
              className="input input-bordered w-full pl-3 pr-16"
              placeholder="Describe what you're looking for..."
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
            />
            {searchText && searchText.length > 10 && (
              <button
                type="button"
                className="absolute inset-y-0 right-12 flex items-center pr-2"
                onClick={() => setSearchText("")}
              >
                <RiCloseCircleLine className="w-5 h-5 text-base-content opacity-70 hover:opacity-100" />
              </button>
            )}
            <button
              type="button"
              className="absolute inset-y-0 right-0 flex items-center pr-3"
              onClick={() => setShowFilters(!showFilters)}
            >
              <RiFilter3Line
                className={`w-5 h-5 transition-all ${
                  showFilters
                    ? "text-primary"
                    : "text-base-content opacity-70 hover:opacity-100"
                }`}
              />
            </button>
          </div>

          {/* Filters Section */}
          {showFilters && (
            <div className="card bg-base-200 p-4 animate-fadeIn">
              <div className="flex flex-wrap gap-4">
                <div className="form-control">
                  <label className="label">
                    <span className="label-text">Content Type</span>
                  </label>
                  <select className="select select-bordered w-full max-w-xs">
                    <option value="all">All Images</option>
                    <option value="photos">Photos</option>
                    <option value="illustrations">Illustrations</option>
                    <option value="vectors">Vectors</option>
                  </select>
                </div>

                <div className="form-control">
                  <label className="label">
                    <span className="label-text">Sort By</span>
                  </label>
                  <select className="select select-bordered w-full max-w-xs">
                    <option value="relevance">Relevance</option>
                    <option value="date">Date Added</option>
                    <option value="likes">Most Liked</option>
                  </select>
                </div>

                <div className="form-control">
                  <label className="label">
                    <span className="label-text">Similarity Threshold</span>
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    className="range range-primary"
                    defaultValue="60"
                  />
                  <div className="w-full flex justify-between text-xs px-2 mt-1">
                    <span>0%</span>
                    <span>50%</span>
                    <span>100%</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div className="flex w-full gap-2 items-center justify-center mb-4">
            <button
              type="submit"
              className="btn text-foreground btn-primary w-full"
              disabled={isSearching || !searchText.trim()}
            >
              {isSearching ? (
                <>
                  {"Searching" + ' "' + searchText + '"'}
                  <span className="loading loading-spinner"></span>
                </>
              ) : (
                <span>
                  {searchedContent == null
                    ? "Search"
                    : `Searched ${searchText}`}
                </span>
              )}
            </button>
          </div>
        </form>
      </div>

      {searchedContent == null && (
        <div className="mt-8 flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-base-300 rounded-lg">
          <RiImageLine className="w-16 h-16 text-base-300" />
          <h3 className="mt-4 text-lg font-medium">No images found</h3>
          <p className="mt-2 text-base-content/70">
            Try searching for something like "forest landscapes" or "urban
            architecture"
          </p>
        </div>
      )}

      {/* Search Results */}
      <div className="columns-2 gap-2">
        {searchedContent &&
          searchedContent.items.map((content) => (
            <Pin content={content} key={content.id}>
              <ImageWithBlurhash image={content} key={content.id} />
            </Pin>
          ))}
      </div>
    </div>
  );
};

export default ImageContextSearch;
