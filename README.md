# How to use
## Choose cleaners
- 우리는 한국어 모델이므로 korean_cleaners를 사용
- config.json에 사용할 text_cleaner 설정
- Remove unnecessary imports from text/cleaners.py
## Python version
- Python: 3.8.16
## Install pytorch
- 파이토치 홈페이지에서 로컬 환경에 맞는 것으로 설치
## Install requirements
```sh
pip install -r requirements.txt
```
만약 설치 도중 에러가 발생한다면 [visual studio build tools](https://visualstudio.microsoft.com/downloads/?q=build+tools) 설치 후 재시도.
## Build monotonic alignment search
```sh
cd monotonic_align
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..
```
## Create datasets
### 단일 화자
- 우리가 사용하는 모델
config.json에서 "n_speakers"는 반드시 0 으로 설정할것
```
path/to/XXX.wav|transcript
```
- Example
```
dataset/001.wav|안녕하세요.
```
### 다중 화자
화자 id는 0부터 시작
```
path/to/XXX.wav|speaker id|transcript
```
- Example
```
dataset/001.wav|0|안녕하세요,
```
## Preprocess
```sh
# Single speaker
python preprocess.py --text_index 1 --filelists path/to/filelist_train.txt path/to/filelist_val.txt --text_cleaners korean_cleaners

# Mutiple speakers
python preprocess.py --text_index 2 --filelists path/to/filelist_train.txt path/to/filelist_val.txt --text_cleaners korean_cleaners
```
이 작업을 처리하고 나면 config.json에 데이터셋을 '전처리한 파일_cleaned.txt'파일로 설정할것
## Small Tips
- 사전학습 모델을 활용할 것 (우리는 카루나 모델 전처리 파일이 슬랙에 있음)
- 만약 vram의 용량이 부족한 경우 (40GB 이하)
- 오디오 파일의 sample rate를 44100Hz로 설정하지 말고 22050Hz로 설정할 것것.
- 데이터 셋의 오디오 파일은 가능하면 짧게 할것. (오디오당 최대 4초를 권장)
## Train
```sh
# Single speaker
python train.py -c <config> -m <folder>

# Our model
python train.py -c checkpoints/karuna/config.json -m karuna

# Mutiple speakers
python train_ms.py -c <config> -m <folder>
```
If you want to train from pretrained model, Place 'G_0.pth' and 'D_0.pth' in destination folder before enter train command.
## Tensorboard
```sh
tensorboard --logdir checkpoints/<folder> --port 6006
```
## Inference
### Jupyter notebook
[infer.ipynb](infer.ipynb)
## Based On
[VITS: Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech](https://github.com/jaywalnut310/vits)
