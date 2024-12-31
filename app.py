from flask import (
    Flask,
    Response,
    render_template,
    request,
    jsonify,
    stream_with_context,
)
from generate_podcast_audio import generate_podcast_audio
from gemini_handler import generate_conversation
from dotenv import load_dotenv
import json
import queue
import threading
import time
import os
import tempfile
import shutil
import uuid
from google_tts import combine_audio_files, OutputFormat, get_supported_stream

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
OUTPUT_FOLDER = "static/output"  # Folder to save generated audio files

# Global dictionary to track audio generation tasks
# Key: task_id, Value: {'queue': Queue, 'status': '...', 'metadata': {...}, 'waiting': True/False, 'file_path': '...', 'timestamp': float}
audio_tasks = {}

# Configuration for cleanup
TASK_EXPIRATION_SECONDS = 3600  # 1 hour (adjust as needed)

# Sentinel object to signal the end of the audio stream
END_OF_STREAM_SENTINEL = object()


def cleanup_old_tasks():
    """Periodically removes old tasks from audio_tasks."""
    while True:
        now = time.time()
        expired_tasks = []
        for task_id, task_info in audio_tasks.items():
            if (
                "timestamp" in task_info
                and now - task_info["timestamp"] > TASK_EXPIRATION_SECONDS
            ):
                expired_tasks.append(task_id)

        for task_id in expired_tasks:
            print(f"Removing expired task: {task_id}")
            del audio_tasks[task_id]  # Remove the task

        time.sleep(600)  # Check every 10 minutes (adjust as needed)


# Start the cleanup thread in the background
cleanup_thread = threading.Thread(target=cleanup_old_tasks, daemon=True)
cleanup_thread.start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate/script", methods=["POST"])
def generate_script():
    try:
        print("Trying to generate script")
        if "topic" not in request.json:
            return jsonify({"success": False, "error": "No topic provided"})
        topic = request.json["topic"]
        settings = request.json["settings"] if "settings" in request.json else {}

        # Generate conversation from topic
        conversation_json = generate_conversation(topic, settings=settings)
        print(conversation_json)
        return jsonify({"success": True, "conversation": conversation_json})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)})


@app.route("/generate/audio", methods=["POST"])
def generate_audio():
    try:
        if not request.json or "conversation" not in request.json:
            return jsonify({"success": False, "error": "No conversation provided"})

        conversation_json = request.json["conversation"]
        settings = request.json.get("settings", {})
        supported_stream_type = request.json.get("supportedStreamType", "audio/mpeg")
        output_format = OutputFormat(settings.get("outputFormat", "wav"))

        # Generate a unique task ID
        task_id = str(uuid.uuid4())

        # Create a queue to hold audio chunks
        audio_queue = queue.Queue()

        # Create the output directory if it doesn't exist
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        # Generate the output file path
        unique_filename = f"podcast-{task_id}.{output_format.value}"
        output_file_path = os.path.join(OUTPUT_FOLDER, unique_filename)

        # Store task information
        audio_tasks[task_id] = {
            "queue": audio_queue,
            "status": "pending",
            "metadata": {},  # You can add initial metadata here if needed
            "waiting": False,
            "file_path": output_file_path,
            "output_format": output_format,
            "timestamp": time.time(),  # Add timestamp
        }

        # Start audio generation in a separate thread
        audio_thread = threading.Thread(
            target=generate_audio_task,
            args=(
                task_id,
                conversation_json,
                settings,
                supported_stream_type,
                audio_queue,
            ),
        )
        audio_thread.daemon = True  # Set as a daemon thread
        audio_thread.start()

        # Return the task ID immediately
        return jsonify({"success": True, "task_id": task_id})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


def generate_audio_task(
    task_id, conversation_json, settings, supported_stream_type, audio_queue
):
    """Generates audio data, puts it into the queue, and saves to file on completion."""
    audio_tasks[task_id]["status"] = "in_progress"
    temp_json_fd, temp_json_path = tempfile.mkstemp(suffix=".json")
    temp_dir = tempfile.mkdtemp()
    audio_files = []  # List to store temporary audio chunk file paths
    output_format = audio_tasks[task_id]["output_format"]

    try:
        with os.fdopen(temp_json_fd, "w") as temp_json_file:
            json.dump(conversation_json, temp_json_file)

        for i, chunk in enumerate(
            generate_podcast_audio(
                temp_json_path, settings=settings, format=output_format
            )
        ):
            temp_audio_file = os.path.join(temp_dir, f"chunk_{i}.{output_format.value}")
            with open(temp_audio_file, "wb") as f:
                f.write(chunk)
            audio_files.append(temp_audio_file)  # Add file path to the list
            supported_type_chunk = get_supported_stream(
                temp_audio_file,
                supported_stream_type=supported_stream_type,
                is_first_chunk=i == 0,
            )
            audio_queue.put(supported_type_chunk)  # Put the audio chunk into the queue
            print(f"Generated chunk {i+1} / {len(audio_files)}")

        # Combine audio files after all chunks are generated
        output_file_path = audio_tasks[task_id]["file_path"]
        combine_audio_files(audio_files, output_file_path, format=output_format)

        # Signal the end of the stream using the sentinel object
        audio_queue.put(END_OF_STREAM_SENTINEL)
        audio_tasks[task_id]["status"] = "completed"

    except Exception as e:
        print(f"Audio generation failed for task {task_id}: {str(e)}")
        audio_tasks[task_id]["status"] = f"failed: {str(e)}"
        # Signal the end of the stream in case of an error
        audio_queue.put(END_OF_STREAM_SENTINEL)

    finally:
        # Cleanup temporary files
        for file in audio_files:
            if os.path.exists(file):
                os.remove(file)
        shutil.rmtree(temp_dir, ignore_errors=True)
        if os.path.exists(temp_json_path):
            os.remove(temp_json_path)
        audio_tasks[task_id]["timestamp"] = time.time()

    print(f"Audio generation for task {task_id} completed.")


def stream_audio(task_id):
    """Streams audio chunks from the queue as they become available."""
    audio_queue = audio_tasks[task_id]["queue"]
    timeout_seconds = 5  # Adjust as needed

    try:
        while True:
            try:
                audio_tasks[task_id]["waiting"] = False  # Not waiting (initially)
                chunk = audio_queue.get(timeout=timeout_seconds)
                if chunk is END_OF_STREAM_SENTINEL:  # End of stream signaled
                    print("End of stream detected (sentinel object)")
                    break
                audio_tasks[task_id]["waiting"] = False  # Not waiting (got a chunk)
                yield chunk

            except queue.Empty:
                # No chunk available within the timeout period
                print("No chunk available, checking task status...")
                audio_tasks[task_id]["waiting"] = True  # Mark as waiting
                if audio_tasks[task_id]["status"] == "completed":
                    print("Audio generation completed, exiting stream loop")
                    break
                elif audio_tasks[task_id]["status"].startswith("failed"):
                    print(f"Audio generation failed: {audio_tasks[task_id]['status']}")
                    break
                else:
                    print("Audio generation still in progress, continuing to wait...")
                    # Continue waiting

    finally:
        if task_id in audio_tasks:
            print(f"Cleaning up task in finally: {task_id}")
            audio_tasks[task_id]["waiting"] = False  # No longer waiting


@app.route("/stream/<task_id>")
def stream(task_id):
    if task_id not in audio_tasks:
        return jsonify({"error": "Task not found"}), 404

    return Response(
        stream_with_context(stream_audio(task_id)), mimetype="audio/mpeg"
    )  # Assuming MP3 output


@app.route("/task_status/<task_id>")
def task_status(task_id):
    if task_id in audio_tasks:
        task_info = audio_tasks[task_id]
        file_path = task_info["file_path"]
        audio_url = None

        if task_info["status"] == "completed":
            # Generate the URL for the saved audio file
            audio_url = f"/static/output/{os.path.basename(file_path)}"

        return jsonify(
            {
                "task_id": task_id,
                "status": task_info["status"],
                "metadata": task_info["metadata"],
                "waiting": task_info["waiting"],
                "audio_url": audio_url,  # Add audio URL if completed
            }
        )
    else:
        return jsonify({"error": "Task not found"}), 404


@app.route("/ack_task/<task_id>", methods=["POST"])
def ack_task(task_id):
    if task_id in audio_tasks:
        print(f"Received acknowledgment for task: {task_id}")
        del audio_tasks[task_id]
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT)
