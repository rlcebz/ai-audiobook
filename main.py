from pathlib import Path
from openai import OpenAI
import fitz
import pydub
import os
import argparse


def get_text(pdf_file_name: str) -> str:
    if ".pdf" in pdf_file_name:
        pdf_file_name = Path(pdf_file_name).stem

    if os.path.isfile(f"{pdf_file_name}.txt"):
        pass
    else:
        with fitz.open(f'{pdf_file_name}.pdf') as doc:
            text = ""
            for page in doc:
                text += page.get_text().strip().strip()
            out = ""
            for t in text.split("\n"):
                out += f"{t.replace(' ', '')} "
            out.replace(" .", ". ")
            out.replace(" ,", ", ")
            with open(f"{pdf_file_name}.txt", "w", encoding="utf-8") as f:
                f.write(out)
    return f"{pdf_file_name}.txt"

def txt_to_mp3(txt_file: str):
    inpt = ""

    with open(txt_file, "r", encoding="utf-8") as book:
        inpt = book.read()

    if len(inpt) > 4096:
        """"""
        i = 0
        f=[]
        while(i<len(inpt)):
            try:
                f.append(inpt[i:i+4095])
                i+=4095
            except:
                f.append(inpt[i:-1])
        chunks = []
        for s in f:
            speech_file_path = Path(__file__).parent / f"{Path(txt_file).stem}/{f.index(s)}.mp3"
            if not os.path.exists(Path(__file__).parent / f"{Path(txt_file).stem}"):
                os.makedirs(Path(__file__).parent / f"{Path(txt_file).stem}")
            if os.path.exists(speech_file_path):
                pass
            else:
                response = client.audio.speech.create(
                model="tts-1",
                voice="onyx",
                input=s
                )
                response.stream_to_file(speech_file_path)
            chunks.append(f"{Path(txt_file).stem}/{f.index(s)}.mp3")
        combined = pydub.AudioSegment.empty()
        chunks.sort(key = lambda x: int(Path(x).stem))
        
        for chunk in chunks:
            combined += pydub.AudioSegment.from_mp3(chunk)
        combined.export(Path(__file__).parent / f"{Path(txt_file).stem}/{Path(txt_file).stem}.mp3", format="mp3")
    else:    
        speech_file_path = Path(__file__).parent / f"{Path(txt_file).stem}/{Path(txt_file).stem}.mp3"
        if not os.path.exists(speech_file_path):
            os.makedirs(speech_file_path)
        response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=inpt
        )
        response.stream_to_file(speech_file_path)
    print("Audiobook saved to ", str(Path(__file__).parent / f"{Path(txt_file).stem}/{Path(txt_file).stem}.mp3"))

def main():
    """"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", type=str, help="OpenAI API key")
    parser.add_argument("--pdf", type=str, help="PDF to convert to mp3")
    opt = parser.parse_args()
    global client
    client = OpenAI(api_key = opt.key)
    text_file = get_text(opt.pdf)
    txt_to_mp3(text_file)
   
if __name__ == "__main__":
    main()