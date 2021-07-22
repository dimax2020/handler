import os
import json


pipe_in = r'/!path!/pipe-out'
pipe_out = r'/!path!/pipe-in'


def main():
    try:
        os.mkfifo(pipe_in)
    except Exception as e:
        if str(e) == "[Errno 17] File exists":
            os.remove(pipe_in)
            os.mkfifo(pipe_in)
        else:
            print(e)
            quit(1)

    request = {"Action": "start", "Str": ""}
    byte_data = json.dumps(request)

    with open(pipe_out, 'rb+', 0) as pipe:
        pipe.write(byte_data.encode())
        pipe.close()

    while True:
        fifo1 = open(pipe_in, 'rb+', 0)
        byte_json = fifo1.read(1024)
        fifo1.close()
        str_json = byte_json.decode()
        data = json.loads(str_json)
        request = {"Str": data["str"] * 2}
        byte_data = json.dumps(request)
        fifo2 = open(pipe_out, 'rb+', 0)
        fifo2.write(byte_data.encode())
        fifo2.close()


if __name__ == "__main__":
    main()
