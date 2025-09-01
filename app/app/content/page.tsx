"use client"
import { useEffect, useState } from "react";
import { SidebarDemo } from "@/components/home/SidebarComponent";
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

interface Background {
  name: string;
  path: string;
}

export default function ContentPage() {
  const [text, setText] = useState("");
  const [backgrounds, setBackgrounds] = useState<Background[]>([]);
  const [selectedBackground, setSelectedBackground] = useState<Background | null>(null);
  const [loading, setLoading] = useState(false);
  const [videoBlob, setVideoBlob] = useState<Blob | null>(null);

  // Fetch available backgrounds on mount
  useEffect(() => {
    const fetchBackgrounds = async () => {
      try {
        const data = await fetchAvailableBackgrounds();
        const backgrounds = data.backgrounds.map((name: string, index: number) => ({
          name,
          path: data.paths[index],
        }));
        setBackgrounds(backgrounds);
        if (backgrounds.length > 0) {
          setSelectedBackground(backgrounds[0]); // Default to first background
        }
      } catch (error) {
        console.error("Error fetching backgrounds:", error);
      }
    };
    fetchBackgrounds();
  }, []);

  // Handle video generation
  const handleGenerateVideo = async () => {
    if (!text.trim() || !selectedBackground) return;
    setLoading(true);
    setVideoBlob(null); // Reset previous video
    try {
      // Generate TTS
      const ttsFilename = await generateTTS(text);
      console.log("TTS generated:", ttsFilename);

      // Generate VTT subtitles
      // VTT subtitles fetches the VTT file from Whisper transcriptions
      // VTT can be then added as track tag on <video> element without burning that
      // on top of the original video as FFMPEG would do
      const vttBlob = await getVTT(ttsFilename);
      console.log("VTT generated");

      // Create video with selected background
      const videoFilename = await createVideo(selectedBackground.name, ttsFilename, ttsFilename.replace('.mp3', '.vtt'));
      console.log("Video created:", videoFilename);

      // Fetch and display the final video
      const videoBlob = await getVideo(videoFilename);
      setVideoBlob(videoBlob);
    } catch (error) {
      console.error("Error generating video:", error);
      alert("Failed to generate video. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-muted">
      <SidebarDemo />
      <main className="flex flex-col flex-1 items-center justify-start gap-8 p-8">
        <div className="w-full max-w-2xl space-y-6">
          <h1 className="text-2xl font-bold tracking-tight">Content Creator</h1>

          {/* Background Selector */}
          <div className="bg-card rounded-lg shadow p-4 border space-y-2">
            <label className="text-sm font-medium">Select Background</label>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="w-full">
                  {selectedBackground ? selectedBackground.name : "Choose Background"}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-full">
                <DropdownMenuLabel>Available Backgrounds</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuRadioGroup
                  value={selectedBackground?.name ?? ""}
                  onValueChange={(bgName) => {
                    const bg = backgrounds.find((b) => b.name === bgName);
                    setSelectedBackground(bg || null);
                  }}
                >
                  {backgrounds.map((bg) => (
                    <DropdownMenuRadioItem key={bg.name} value={bg.name}>
                      {bg.name}
                    </DropdownMenuRadioItem>
                  ))}
                </DropdownMenuRadioGroup>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>

          {/* Text Input */}
          <div className="bg-card rounded-lg shadow p-4 border space-y-2">
            <label className="text-sm font-medium">Enter Your Content</label>
            <textarea
              className="w-full h-32 p-3 border border-input bg-background text-sm rounded-md focus:outline-none focus:ring-2 focus:ring-primary resize-none"
              placeholder="Type your content here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              disabled={loading}
            />
          </div>

          {/* Generate Button */}
          <div className="flex justify-center">
            <Button
              onClick={handleGenerateVideo}
              disabled={!text.trim() || !selectedBackground || loading}
              className="w-full max-w-xs"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <span className="animate-spin h-4 w-4 border-2 border-t-transparent border-white rounded-full" />
                  Generating...
                </span>
              ) : (
                "Generate Video"
              )}
            </Button>
          </div>

          {/* Video Display */}
          {videoBlob && (
            <div className="bg-card rounded-lg shadow p-4 border flex flex-col items-center space-y-2">
              <h3 className="text-md font-medium">Generated Video</h3>
              <video
                className="w-full max-w-4xl rounded-lg border border-neutral-200 dark:border-neutral-700"
                controls
                autoPlay
                muted
              >
                <source src={URL.createObjectURL(videoBlob)} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

// API Helper Functions
async function fetchAvailableBackgrounds() {
  const response = await fetch("/api/py/available-backgrounds");
  if (!response.ok) throw new Error("Failed to fetch backgrounds");
  return response.json();
}

async function generateTTS(text: string): Promise<string> {
  const response = await fetch("/api/py/generate_tts", {
    method: "POST",
    headers: { "Content-Type": "text/plain" },
    body: text,
  });
  if (!response.ok) throw new Error("Failed to generate TTS");
  const data = await response.json();
  return data.filename.split('/').pop();
}

async function getVTT(filename: string): Promise<Blob> {
  const response = await fetch(`/api/py/get_subtitles/?filename=${encodeURIComponent(filename)}`);
  if (!response.ok) throw new Error("Failed to generate VTT");
  return response.blob();
}

async function createVideo(backgroundFile: string, audioFile: string, subtitlesFile: string): Promise<string> {
  const response = await fetch(
    `/api/py/create_video/?background_file=${encodeURIComponent(backgroundFile)}&audio_file=${encodeURIComponent(audioFile)}&subtitles_file=${encodeURIComponent(subtitlesFile)}`,
    { method: "POST" }
  );
  if (!response.ok) throw new Error("Failed to create video");
  const data = await response.json();
  return data.filename;
}

async function getVideo(filename: string): Promise<Blob> {
  const response = await fetch(`/api/py/get_video/${encodeURIComponent(filename)}`);
  if (!response.ok) throw new Error("Failed to fetch video");
  return response.blob();
}