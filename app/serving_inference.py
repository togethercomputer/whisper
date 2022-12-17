import os
import base64
import logging
from io import BytesIO
from typing import Dict
import torch
import whisper

from transformers.pipelines.audio_utils import ffmpeg_read
from together_worker.fast_inference import FastInferenceInterface
from together_web3.together import TogetherWeb3, TogetherClientOptions
from together_web3.computer import LanguageModelInferenceChoice, RequestTypeLanguageModelInference

class FastWhisper(FastInferenceInterface):
    def __init__(self, model_name: str, args=None) -> None:
        args = args if args is not None else {}
        super().__init__(model_name, args)
        self.device = args.get("device", "cuda")
        self.model = whisper.load_model("large", device=self.device, download_root=os.environ.get("MODEL_DIR"))

    def dispatch_request(self, args, env) -> Dict:
        try:
            inputs = args[0]["audio_base64"]
            if inputs.startswith('data:audio/'):
                delim_index = inputs.find(';base64,')
                if delim_index >= 0:
                    inputs = base64.b64decode(inputs[(delim_index + 8):])
                else:
                    inputs = bytes(inputs, 'utf-8')
            else:
                inputs = base64.b64decode(inputs)
            audio_nparray = ffmpeg_read(inputs, 16000)
            audio_tensor = torch.from_numpy(audio_nparray)
            result = self.model.transcribe(audio_nparray)

            choices = [LanguageModelInferenceChoice(result['text'])]
            return {
                "result_type": RequestTypeLanguageModelInference,
                "choices": choices,
            }
        except Exception as e:
            logging.exception(e)
            return {
                "result_type": "error",
                "value": str(e),
            }

if __name__ == "__main__":
    coord_url = os.environ.get("COORD_URL", "127.0.0.1")
    coordinator = TogetherWeb3(
        TogetherClientOptions(reconnect=True),
        http_url=os.environ.get("COORD_HTTP_URL", f"http://{coord_url}:8092"),
        websocket_url=os.environ.get("COORD_WS_URL", f"ws://{coord_url}:8093/websocket"),
    )
    fip = FastWhisper(model_name=os.environ.get("MODEL", "whisper"), args={
        "auth_token": os.environ.get("AUTH_TOKEN"),
        "coordinator": coordinator,
        "device": os.environ.get("DEVICE", "cuda"),
        "gpu_num": 1 if torch.cuda.is_available() else 0,
        "gpu_type": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "gpu_mem": torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else None,
        "group_name": os.environ.get("GROUP", "group1"),
        "worker_name": os.environ.get("WORKER", "worker1"),
    })
    fip.start()
