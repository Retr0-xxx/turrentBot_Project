
import server
import video
import threading

if __name__ == "__main__":
    # Create a thread for the server
    server_thread = threading.Thread(target=server.startServer)

    # Create a thread for video streaming
    video_thread = threading.Thread(target=video.startVideo)

    # Start both threads
    server_thread.start()
    video_thread.start()

    # Optionally, wait for both threads to complete
    server_thread.join()
    video_thread.join()