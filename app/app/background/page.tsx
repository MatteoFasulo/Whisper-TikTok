"use client"
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { SidebarDemo } from "@/components/home/SidebarComponent";

interface Background {
  name: string;
  path: string;
}

export default function Page() {
  const [backgrounds, setBackgrounds] = useState<Background[]>([]);
  const [selectedBackground, setSelectedBackground] = useState<Background>();
  const [inputUrl, setInputUrl] = useState("");
  const [downloading, setDownloading] = useState(false);

  // Fetch backgrounds
  const fetchBackgrounds = async () => {
    const data = await fetchAvailableBackgrounds();
    const backgrounds = data.backgrounds;
    const paths = data.paths;
    setBackgrounds(
      backgrounds.map((name: string, index: number) => ({
        name,
        path: paths[index],
      }))
    );
  };

  useEffect(() => {
    fetchBackgrounds();
  }, []);

  // Download handler
  const handleDownload = async () => {
    if (!inputUrl) return;
    setDownloading(true);
    try {
      await downloadBackground(inputUrl);
      setInputUrl("");
      await fetchBackgrounds();
      // Optionally auto-select the new background if you know its name
      // setSelectedBackground(backgrounds.find(b => b.name === data.file_name));
    } catch (error) {
      console.error("Error downloading background:", error);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="flex min-h-screen">
      <SidebarDemo />
      <main className="flex flex-col flex-1 items-center justify-start gap-8 p-8">
        <div className="w-full max-w-2xl space-y-4">
          <h1 className="text-2xl font-bold">Background Video Manager</h1>
          <div className="flex items-center gap-2 bg-card rounded-lg p-4 border">
            <input
              type="text"
              placeholder="Paste YouTube or video URL..."
              className="flex-1 px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              value={inputUrl}
              onChange={e => setInputUrl(e.target.value)}
              disabled={downloading}
            />
            <Button
              variant="default"
              className="ml-2"
              onClick={handleDownload}
              disabled={!inputUrl || downloading}
            >
              {downloading ? (
                <span className="flex items-center gap-2">
                  <span className="animate-spin h-4 w-4 border-2 border-t-transparent rounded-full" />
                  Downloading...
                </span>
              ) : (
                "Download"
              )}
            </Button>
          </div>
        </div>

        <div className="w-full max-w-2xl space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Select Background</h2>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline">Choose</Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-fit">
                <DropdownMenuLabel>Backgrounds</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuRadioGroup
                  value={selectedBackground?.name ?? ""}
                  onValueChange={bg => {
                    setSelectedBackground(backgrounds.find(b => b.name === bg));
                  }}
                >
                  {backgrounds.map(bg => (
                    <DropdownMenuRadioItem key={bg.name} value={bg.name}>
                      {bg.name}
                    </DropdownMenuRadioItem>
                  ))}
                </DropdownMenuRadioGroup>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <div className="border-b" />
        </div>

        {selectedBackground && (
          <div className="w-full max-w-4xl bg-card rounded-lg p-4 border flex flex-col items-center">
            <h3 className="text-md font-medium mb-2">{selectedBackground.name}</h3>
            <VideoPlayer
              key={selectedBackground.name}
              backgroundPath={`http://localhost:8000/api/py/background/${encodeURIComponent(
                selectedBackground.name
              )}?t=${Date.now()}`}
            />
          </div>
        )}
      </main>
    </div>
  );
}

function VideoPlayer({ backgroundPath }: { backgroundPath: string }) {
  const [loading, setLoading] = useState(true);

  return (
    <div className="relative w-full max-w-3xl">
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center z-10 rounded-lg">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500" />
        </div>
      )}
      <video
        className="w-full rounded-lg border dark:border-neutral-700"
        controls
        autoPlay
        onLoadStart={() => setLoading(true)}
        onCanPlay={() => setLoading(false)}
      >
        <source src={backgroundPath} type="video/mp4" />
        <track
          src="/path/to/captions.vtt"
          kind="subtitles"
          srcLang="en"
          label="English"
        />
        Your browser does not support the video tag.
      </video>
    </div>
  );
}

async function fetchAvailableBackgrounds() {
  const response = await fetch("/api/py/available-backgrounds");
  if (!response.ok) {
    throw new Error("Failed to fetch backgrounds");
  }
  const data = await response.json();
  return data;
}

async function downloadBackground(url: string) {
  const response = await fetch(
    `/api/py/download-video/?url=${encodeURIComponent(url)}`
  );
  if (!response.ok) {
    throw new Error("Failed to download background");
  }
  const data = await response.json();
  return data;
}