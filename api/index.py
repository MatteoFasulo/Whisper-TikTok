"""API for Whisper-TikTok."""

from pathlib import Path

from fastapi import Body, FastAPI, Header, Query, Response
from fastapi.responses import JSONResponse

from whisper_tiktok import subtitle_creator, text_to_speech, video_creator, video_downloader, video_prepare

HOME = Path.cwd()
media_folder = HOME / "media"
output_folder = HOME / "output"
video_folder = HOME / "background"

media_folder.mkdir(exist_ok=True)
output_folder.mkdir(exist_ok=True)
video_folder.mkdir(exist_ok=True)

app = FastAPI(docs_url="/api/py/docs")


@app.get("/api/py/download-video")
async def download_video(url: str = Query(...)):
    """Download a video from a given URL."""
    status, info = video_downloader.download_video(url)
    if not status:
        return JSONResponse(status_code=400, content={"message": info})
    return JSONResponse(
        status_code=200,
        content={"message": "Video downloaded successfully", "file_path": info},
    )


@app.get("/api/py/available-backgrounds")
async def available_backgrounds():
    """Get a list of available backgrounds."""
    backgrounds = list(video_folder.glob("*"))
    return JSONResponse(
        status_code=200,
        content={
            "backgrounds": [bg.name for bg in backgrounds],
            "paths": [str(bg.absolute()) for bg in backgrounds],
        },
    )


@app.get("/api/py/background/{filename}")
async def stream_video(filename: str, range_header: str = Header(None)):
    """Stream a video file with support for range requests."""
    path = video_folder / filename
    if not path.exists():
        return Response(status_code=404)

    file_size = path.stat().st_size
    start, end = 0, file_size - 1  # Serve the entire file if no range is specified

    if range_header:
        range_header = range_header.replace("bytes=", "")
        parts = range_header.split("-")
        start = int(parts[0])
        end = (
            int(parts[1]) if parts[1] else file_size - 1
        )  # Serve to the end if no end is specified

    with open(path, "rb") as f:
        f.seek(start)
        data = f.read(end - start + 1)

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(end - start + 1),
        "Content-Type": "video/mp4",
    }

    status_code = (
        206 if range_header else 200
    )  # Return 200 OK if serving the entire file
    return Response(data, status_code=status_code, headers=headers)


@app.post("/api/py/generate_tts")
async def generate_tts(
    text: str = Body(...),
    outfile: str = Query("output.mp3"),
    voice: str = Query("en-US-ChristopherNeural"),
):
    """Convert text to speech."""
    output_mp3 = media_folder / outfile
    await text_to_speech.tts(text=text, outfile=output_mp3, voice=voice)
    return JSONResponse(
        status_code=200,
        content={"message": "TTS generated successfully", "filename": str(output_mp3)},
    )

@app.get("/api/py/get_tts/{filename}")
async def get_tts(filename: str):
    """Get the generated TTS audio file."""
    mp3_path = media_folder / filename
    if not mp3_path.exists():
        return JSONResponse(
            status_code=404, content={"message": "Audio file not found"}
        )
    return Response(
        content=mp3_path.read_bytes(), media_type="audio/mpeg"
    )


@app.get("/api/py/get_subtitles")
async def transcribe_audio(
    filename: str = Query(...),
    model: str = "base",
    non_english: bool = False,
    uuid: str = "media",
):
    """Transcribe audio to generate subtitles."""
    mp3_path = media_folder / filename
    if not mp3_path.exists():
        return JSONResponse(
            status_code=404, content={"message": "Audio file not found"}
        )

    whisper_model = video_creator.get_whisper_model(model, non_english)

    subtitle_creator.srt_create(
        whisper_model,
        mp3_filename=mp3_path,
        out_folder=media_folder,
        uuid=uuid,
        font="Lexend Bold",
        sub_position=5,
        font_size=21,
        font_color="FFFFFF",
    )

    vtt_filename = media_folder / f"{uuid}.vtt"

    headers = {
        "Content-Disposition": f"attachment; filename={vtt_filename.name}",
        "Content-Type": "text/vtt",
    }

    return Response(
        content=vtt_filename.read_bytes(), media_type="text/vtt", headers=headers
    )

@app.post("/api/py/create_video")
async def create_video(
    background_file: str = Query(...),
    audio_file: str = Query(...),
    subtitles_file: str = Query(...),
):
    """Create a video from background, audio, and subtitles."""
    video_path = video_folder / background_file
    if video_path.exists():
        return JSONResponse(
            status_code=200, content={"message": "Video already exists", "path": str(video_path)}
        )

    print("Background video:", video_path)
    print("Audio file:", audio_file)
    print("Subtitles file:", subtitles_file)

    # Create video using the provided background, audio, and subtitles
    video_prepare.prepare_background(
        mp4_background_filename=video_path,
        mp3_filename=Path(audio_file),
        ass_filename=Path(subtitles_file),
        out_folder=video_folder,
        uuid="output"
    )

@app.get("/api/py/get_video/{filename}")
async def get_video(filename: str):
    """Get the generated video file."""
    video_path = video_folder / filename
    if not video_path.exists():
        return JSONResponse(
            status_code=404, content={"message": "Video file not found"}
        )
    return Response(
        content=video_path.read_bytes(), media_type="video/mp4"
    )