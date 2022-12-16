# whisper

Container for serving [OpenAI's Whisper](https://huggingface.co/openai/whisper-large) on Together Computer.

To bring up a standalone node:

```console
mkdir .together
docker run --rm --gpus all \
  -e NUM_WORKERS=auto \
  -e CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
  -v $PWD/.together:/home/user/.together \
  -it togethercomputer/whisper /usr/local/bin/together start \
    --worker.model whisper --config /home/user/cfg.yaml --color
```

To query model:

```console
curl -X POST -H 'Content-Type: application/json' \
  https://staging.together.xyz/api/inference \
  -d "{ \"model\": \"whisper\", \"audio_base64\": \"`base64 -in gettysburg.wav`\" }"
```

```console
{"prompt":[null],"model":"whisper","model_owner":"","tags":{},"num_returns":1,"args":{"model":"whisper"},"output":{"choices":[{"text":" Four score and seven years ago, our fathers brought forth on this continent a new nation, conceived in liberty and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation or any nation so conceived and so dedicated can long endure."}],"result_type":"language-model-inference"},"status":"finished","subjobs":[]}
```
