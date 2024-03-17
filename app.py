import IPython.display as ipd
import torch
import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
from pydantic import BaseModel
from scipy.io.wavfile import write
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import uvicorn
import time

app = FastAPI()
# -------------------AI모델---------------------------
class vits():
    def __init__(self, checkpoint_path, config_path):
        self.hps = utils.get_hparams_from_file(config_path)
        self.spk_count = self.hps.data.n_speakers
        self.net_g = SynthesizerTrn(
            len(symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            n_speakers=self.hps.data.n_speakers,
            **self.hps.model).cuda()
        _ = self.net_g.eval()
        _ = utils.load_checkpoint(checkpoint_path, self.net_g, None)

    def get_text(self, text, hps):
        text_norm = text_to_sequence(text, hps.data.text_cleaners)
        if hps.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = torch.LongTensor(text_norm)
        return text_norm

    async def infer(self, text, spk_id=0):
        ipd.clear_output()
        stn_tst = self.get_text(text, self.hps)
        with torch.no_grad():
            x_tst = stn_tst.cuda().unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
            sid = torch.LongTensor([spk_id]).cuda()
            audio = self.net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
        write(f'infer/test.wav', self.hps.data.sampling_rate, audio)
tts = vits('checkpoints/finetune/G_44000.pth', 'checkpoints/finetune/config.json')
# --------------------------------------------------------------------------------
class ChatData(BaseModel):
    chat:str
@app.post("/getmessage")
async def get_message(data: ChatData):
    start = time.time()
    print('start processing!', start)
    msg = data.chat
    print('chat:', msg)
    await tts.infer(msg)
    print('Data Generated Complete')
    wav_file_path = "infer/test.wav"
    print(f'Data Generated time: {time.time()-start}')
    return FileResponse(wav_file_path, media_type="audio/wav")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9090)