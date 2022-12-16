# whisper

To bring up a standalone node:

```console
mkdir .together
docker run --rm --gpus all \
  -e NUM_WORKERS=auto \
  -e CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
  -v $PWD/.together:/home/user/.together \
  -it togethercomputer/whisper /usr/local/bin/together start \
    --worker.model whisper -f /home/user/cfg.yaml --color
```

Query model

```console
curl -X POST -H 'Content-Type: application/json' https://staging.together.xyz/api/inference -d "{ \"model\": \"whisper\", \"audio_base64\": \"`base64 -in gettysburg.wav`\" }" > output.json
```
