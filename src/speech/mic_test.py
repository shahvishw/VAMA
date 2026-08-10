import pyaudio
import math

audio = pyaudio.PyAudio()

CHUNK = 1024
RECORD_SECONDS = 3
FORMAT = pyaudio.paInt16


def calculate_rms(data):
    samples = len(data) // 2

    if samples == 0:
        return 0

    total = 0

    for i in range(0, len(data), 2):
        sample = int.from_bytes(
            data[i:i + 2],
            byteorder="little",
            signed=True
        )

        total += sample * sample

    return math.sqrt(total / samples)


for index in range(audio.get_device_count()):

    device = audio.get_device_info_by_index(index)

    if device["maxInputChannels"] <= 0:
        continue

    print("\n--------------------------------")
    print(f"Index : {index}")
    print(f"Name  : {device['name']}")
    print(f"Rate  : {device['defaultSampleRate']}")
    print("--------------------------------")

    try:

        stream = audio.open(
            format=FORMAT,
            channels=1,
            rate=int(device["defaultSampleRate"]),
            input=True,
            input_device_index=index,
            frames_per_buffer=CHUNK
        )

        print("Speak now for 3 seconds...")

        maximum_volume = 0

        for _ in range(
            int(device["defaultSampleRate"] / CHUNK * RECORD_SECONDS)
        ):

            data = stream.read(
                CHUNK,
                exception_on_overflow=False
            )

            volume = calculate_rms(data)

            maximum_volume = max(
                maximum_volume,
                volume
            )

        stream.stop_stream()
        stream.close()

        print(f"Maximum volume detected: {maximum_volume:.2f}")

    except Exception as error:

        print(f"Could not test device: {error}")


audio.terminate()