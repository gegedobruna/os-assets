"""
albkinema.co — Themelimi Osman batch downloader (eps 180-200)
==============================================================
Just loops through URLs and runs yt-dlp with parallel fragments.
No browser, no detection — straightforward.

Requires:
    winget install yt-dlp   (or pip install yt-dlp)
"""

import subprocess
import os
import time
import argparse

OUTPUT_DIR = "osman_episodes"

# all confirmed URLs. f2 = 1080p, f1 = 720p. script forces 720p below.
EPISODE_URLS: dict[int, str] = {
    180: "https://sil5.stellarforgeinnovation.online/v4/is3/qapaes/index-f2-v1-a1.txt",
    181: "https://smho.luminarstrategyhub.site/v4/rqz/oc6cm1/index-f2-v1-a1.txt",
    182: "https://sunl.silverskymedia.cyou/v4/pk8/u8g8x6/index-f2-v1-a1.txt",
    183: "https://shkn.stellarpathventures.space/v4/ic/mp5pts/index-f2-v1-a1.txt",
    184: "https://s6p9.gametech.cfd/v4/miy/u8g8mi/index-f2-v1-a1.txt",
    185: "https://s3wh.meliora.cyou/v4/x6b/9jxjx5/index-f2-v1-a1.txt",
    186: "https://srcf.fitnessfanatics.cyou/v4/hz/lnbnmf/index-f1-v1-a1.txt",
    187: "https://185.237.106.10/v4/oOgmQwgtwmModGc-idiFHA/1782354670/vz1/mp5pwk/index-f1-v1-a1.m3u8",
    188: "https://sknw.merridianproductions.store/v4/6hf/mp5pwy/index-f1-v1-a1.txt",
    189: "https://srcf.individualshowcase.cyou/v4/36/sdfdmt/index-f2-v1-a1.txt",
    190: "https://s9r1.zenithflowengineering.shop/v4/ic/vbdb8y/index-f2-v1-a1.txt",
    191: "https://sipt.mindspireleadership.space/v4/ty/glvlyp/index-f2-v1-a1.txt",
    192: "https://s3wh.lyonic.cyou/v4/x68/69a9bx/index-f2-v1-a1.txt",
    193: "https://sil5.merridianart.space/v4/mik/ikwkma/index-f2-v1-a1.txt",
    194: "https://sr81.aurorafieldventures.shop/v4/3vi/vbdbtm/index-f2-v1-a1.txt",
    195: "https://srcf.lumintrixdigital.online/v4/3vi/vbdbv6/index-f2-v1-a1.txt",
    196: "https://sil5.zenlithsustainables.cyou/v4/epu/5yobwy/index-f2-v1-a1.txt",
    197: "https://185.237.106.178/v4/9d8lGZRI1ohCL6IJCkX9UA/1782736777/db/prynoc/index-f1-v1-a1.m3u8",
    198: "https://sd8g.mindspireleadership.space/v4/9a/sdfrdg/index-f1-v1-a1.txt",
    199: "https://sipt.velonaacademy.online/v4/36/5yobxi/index-f1-v1-a1.txt",
    200: "https://sxix.luminarygroupdigital.online/v4/5c/69akda/index-f2-v1-a1.txt",
    201: "https://185.237.106.76/v4/oA_O9h2Fd05v5-1zUUvxCQ/1782352881/rqz/lnbjtj/index-f2-v1-a1.m3u8",
    202: "https://s5zt.creativegrowthworld.site/v4/9a/u8gczf/index-f2-v1-a1.txt",
    203: "https://ssu5.fitnessfanatic.sbs/v4/s93/qap6np/index-f1-v1-a1.txt",
    204: "https://s8v3.fitnessfanatic.sbs/v4/kdv/ikw3iq/index-f2-v1-a1.txt",
    205: "https://soq6.gameaddict.site/v4/ek/d3ix8m/index-f2-v1-a1.txt",
    206: "https://s8v3.silverlineinnovation.shop/v4/m9/bh3jhi/index-f2-v1-a1.txt",
    207: "https://sxix.velonaacademy.online/v4/rw/jvs6fn/index-f1-v1-a1.txt",
    208: "https://s8v3.vinturastudios.shop/v4/pk8/d3ixfk/index-f2-v1-a1.txt",
    209: "https://spo3.moonstreamspace.space/v4/xq/mp58cw/index-f2-v1-a1.txt",
    210: "https://s3ae.fitnessessentials.cfd/v4/ic/tfupkn/index-f2-v1-a1.txt",
    211: "https://sxix.greenvalleynetworks.sbs/v4/rw/xstq5h/index-f2-v1-a1.txt",
    212: "https://s8v3.xylonadynamics.cyou/v4/js/69a3z1/index-f2-v1-a1.txt",
    213: "https://185.237.106.219/v4/yM5cTDp0jA_S00kjxMJBvQ/1782353101/pp/ikwtxo/index-f2-v1-a1.m3u8",
    214: "https://s3wh.amberleaftravel.online/v4/ic/69a3xm/index-f2-v1-a1.txt",
    215: "https://silu.digitalfuture.cyou/v4/mik/ikwtij/index-f2-v1-a1.txt",
    216: "https://silu.zenithnetworklabs.site/v4/urp/xst5hn/index-f2-v1-a1.txt",
    217: "https://sil5.merridianproductions.store/v4/c5u/xst5lb/index-f2-v1-a1.txt",
    218: "https://s3ae.nuvistar.online/v4/rw/ikwzjd/index-f2-v1-a1.txt",
    219: "https://sskt.fitnessfanatics.cyou/v4/onm/31kuek/index-f2-v1-a1.txt",
}


def to_720p(url: str) -> str:
    """force 720p by swapping f2 → f1 if needed."""
    return url.replace("index-f2-", "index-f1-")


def already_downloaded(ep: int) -> bool:
    """skip eps that have a finished .mp4 AND no leftover .part files."""
    path = f"{OUTPUT_DIR}/osman_ep{ep:03d}.mp4"
    if not (os.path.exists(path) and os.path.getsize(path) > 100_000_000):  # >100MB
        return False
    # check for leftover fragment files — means previous run didn't finish merging
    leftover_parts = [
        f for f in os.listdir(OUTPUT_DIR)
        if f.startswith(f"osman_ep{ep:03d}.mp4.part")
    ]
    if leftover_parts:
        print(f"  [ep {ep}] found {len(leftover_parts)} leftover .part files — needs redo")
        return False
    return True


def download(ep: int, url: str) -> bool:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_tpl = f"{OUTPUT_DIR}/osman_ep{ep:03d}.%(ext)s"
    stream_url = to_720p(url)
    
    print(f"\n{'='*60}")
    print(f"  ep {ep}")
    print(f"  {stream_url}")
    print(f"{'='*60}\n")

    cmd = [
    "yt-dlp",
    "--referer", "https://koskinema.uns.wtf/",
    "--concurrent-fragments", "1",
    "--hls-prefer-native",
    "--retries", "10",
    "--fragment-retries", "10",
    "-o", output_tpl,
    stream_url,
    ]
    result = subprocess.run(cmd)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=str, required=True,
                        help="comma-separated episode numbers, e.g. 205,206,207")
    parser.add_argument("--force", action="store_true",
                        help="re-download even if file already exists")
    args = parser.parse_args()

    ep_list = [int(x.strip()) for x in args.episodes.split(",")]

    failed = []
    skipped = []

    for ep in ep_list:
        if ep not in EPISODE_URLS:
            print(f"[ep {ep}] no URL stored — skipping")
            failed.append(ep)
            continue

        if not args.force and already_downloaded(ep):
            print(f"[ep {ep}] already downloaded — skipping (use --force to redo)")
            skipped.append(ep)
            continue

        ok = download(ep, EPISODE_URLS[ep])  # type: ignore[arg-type]
        if not ok:
            failed.append(ep)
            print(f"  !! ep {ep} failed")

        time.sleep(2)

    print("\n" + "="*60)
    print("  summary")
    print("="*60)
    if skipped:
        print(f"  skipped (already done): {skipped}")
    if failed:
        print(f"  failed:                 {failed}")
    if not failed:
        print(f"  all done ✓")


if __name__ == "__main__":
    main()
