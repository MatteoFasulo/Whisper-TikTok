# Getting Started

To get started with this NextJS project, you first need to spin-up the python fastAPI server.

Activate the python virtual environment and then run the following command:

```bash
uvicorn api.index:app --reload
```

Then, open a new terminal and run the following command to start the Next.js development server:

```bash
npm run dev
```

This will start the server on [http://localhost:3000](http://localhost:3000). You can view the application in your web browser.

## Fast API

The FastAPI server will be running on [http://localhost:8000](http://localhost:8000). You can view the API documentation at [http://localhost:8000/api/py/docs](http://localhost:8000/api/py/docs).

The main idea of the Fast API endpoint is to expose the functionality of the underlying python library with GET and POST requests that can be handled by the Next.js frontend.

The logic should be simple, whenever we need to perform an operation that produces an artifact (e.g., an output or processed file), we should define a corresponding API endpoint with a POST request that only informs about the outcome of the operation. After creating such artifact, we define a GET request that allows the frontend to retrieve the artifact (e.g., a Blob or file).

>Note: right now, some API endpoints are not fully implementing the aforementioned style of GET-POST requests. This porting is still on development and subject to change. For example, there are some calls inside the NextJS frontend without modular API URLs which need to be replaced.

### Points to Consider

* should we use the `Query` approach when dealing with optional query parameters in the API or directly calling a `/api/py/{function}/{item}` endpoint?
* I would first move the project to such python-based structure before fully migrating to JavaScript. If the project structure is modular enough, the two parts can be developed in parallel, and working on new features would only require adding more endpoints and the corresponding frontend logic (which is a strong advantage).

## Migrating from Python to full JavaScript

For migrating completely from Python to NextJS, a couple of dependencies need to be replaced or re-implemented in JavaScript. This includes:

* The Fast API endpoints should be re-implemented as Next.js API routes or dropped if not needed.
* The EdgeTTS Python library should be replaced with a JavaScript equivalent (e.g., https://www.npmjs.com/package/@andresaya/edge-tts).
* The Whisper ASR functionality should be re-implemented using a JavaScript library or API. This could involved using some binding of Whisper directly in JavaScript or switching to WebGPU with ONNX runtime backend.
  * what is important is the ability of the model to run efficiently on any hardware (e.g., CPU or GPU), without relying on additional dependencies. 
  * the new model should keep the same functionality as the previous one, namely transcribing audio to text with segment and word level timestamps. Check [stable-ts](https://github.com/jianfch/stable-ts) python library for a quick check of the features and then have a look at `subtitle_creator.py` file for the needed features. The main features are about splitting by gap and maximum words per sequence as to do not have a wall of text as subtitles.
* For creating the final video, FFMPEG is still needed and suggested to be used as a separate service that can be called from the Next.js API routes. A replacement for FFMPEG in the JavaScript ecosystem is not suggested due to performance and compatibility issues. I would personally stick to FFMPEG.