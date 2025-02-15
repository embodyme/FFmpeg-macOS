from argparse import ArgumentParser
from multiprocessing import cpu_count
import pathlib
import sys
import os


def execute(command: str):
    print(f"Execute: {command}.")
    os.system(command)


if __name__ == "__main__":
    parser = ArgumentParser(description="Configure & Make & Install FFmpeg.")
    parser.add_argument("--ffmpeg_dir", type=str, default=os.getcwd(), help='indicate FFmpeg dir.')
    parser.add_argument("--target_dir", type=str, default=os.getcwd(), help='indicate target dir.')
    args = parser.parse_args()
    ffmpeg_dir = pathlib.Path(args.ffmpeg_dir).absolute()
    target_dir = pathlib.Path(args.target_dir).absolute()
    print(f"Compile... {ffmpeg_dir}")


    def clean():
        print("Clean project.")
        execute(f"cd {ffmpeg_dir} && make clean && make distclean")


    def make(arch: str):
        n_cpu = cpu_count()
        print("Configure project.")
        execute(
            f"cd {ffmpeg_dir} && ./configure --enable-cross-compile --prefix={target_dir / ('install_' + arch + '/')} "
            f"--install-name-dir=@rpath --enable-shared --disable-static --enable-libvorbis --enable-libvpx "
            f"--enable-pic --disable-doc --enable-debug --enable-runtime-cpudetect --enable-asm --enable-x86asm "
            f"--target-os=darwin --enable-ffmpeg --disable-ffplay --enable-ffprobe --disable-alsa --enable-avcodec "
            f"--enable-avdevice --enable-avformat --enable-avfilter --disable-postproc --enable-swresample --enable-swscale "
            f"--disable-libaom --disable-libass --disable-avisynth --disable-bzlib --disable-libfdk-aac --disable-libfontconfig "
            f"--disable-libfreetype --disable-libfribidi --disable-iconv --disable-libilbc --disable-lzma --disable-libmp3lame --disable-libmodplug "
            f"--disable-cuda --disable-nvenc --disable-nvdec  --disable-cuvid --disable-ffnvcodec --disable-opencl --disable-opengl --disable-libopenh264 "
            f"--disable-libopenjpeg --disable-openssl --disable-libopus --disable-sdl2 --disable-libsnappy --disable-libsoxr --disable-libspeex --disable-libssh "
            f"--disable-libtensorflow --disable-libtesseract --disable-libtheora --disable-libvorbis --enable-libvpx --disable-libwebp --disable-libx264 "
            f"--disable-libx265 --disable-libxml2 --disable-zlib --disable-vdpau "
            # f"--enable-libvorbis --enable-libvpx "
            f"--arch={arch} --cc='clang -arch {arch}'"
        )
        print(f"Make project ({n_cpu} threads).")
        execute(f"cd {ffmpeg_dir} && make -j{n_cpu}")
        print(f"Install project.")
        execute(f"cd {ffmpeg_dir} && make install")


    
    print("----------x86_64----------")
    clean()
    make("x86_64")
    print("----------arm64----------")
    clean()
    make("arm64")
