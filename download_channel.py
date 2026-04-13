#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path

DEFAULT_CHANNEL = "https://www.youtube.com/@Lafilmotecamaldita/videos"


def get_channel_url(passed_url: str | None) -> str:
    if passed_url:
        return passed_url.strip()

    print(f"Default channel: {DEFAULT_CHANNEL}")
    user_input = input("Enter another channel URL, or press Enter to use the default: ").strip()
    return user_input if user_input else DEFAULT_CHANNEL


def check_yt_dlp_installed() -> None:
    try:
        subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        raise SystemExit(
            "yt-dlp is not installed.\n"
            f"Install it with:\n  {sys.executable} -m pip install -U --pre \"yt-dlp[default]\"\n"
        ) from exc


def build_command(
    channel_url: str,
    output_dir: Path,
    archive_file: Path,
    ffmpeg_location: str | None,
    cookies_file: Path | None,
) -> list[str]:
    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--ignore-errors",
        "--continue",
        "--no-overwrites",
        "--retries", "10",
        "--fragment-retries", "10",
        "--download-archive", str(archive_file),
        "--sleep-interval", "5",
        "--max-sleep-interval", "10",
        "--remote-components", "ejs:github",
        "--js-runtimes", "deno",
        "-f", "bv*+ba/b",
        "--merge-output-format", "mkv",
        "--embed-metadata",
        "--write-thumbnail",
        "--convert-thumbnails", "jpg",
        "-o",
        str(output_dir / "%(channel|uploader)s/%(upload_date>%Y-%m-%d)s - %(title)s [%(id)s].%(ext)s"),
        channel_url,
    ]

    if cookies_file is not None:
        cmd.extend(["--cookies", str(cookies_file)])

    if ffmpeg_location:
        cmd.extend(["--ffmpeg-location", ffmpeg_location])

    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download all videos from a YouTube channel in the best available quality."
    )
    parser.add_argument(
        "channel_url",
        nargs="?",
        help="Optional channel URL. If omitted, the script will ask interactively.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="downloads",
        help='Folder to save videos into (default: "downloads")',
    )
    parser.add_argument(
        "--archive-file",
        default="downloaded_archive.txt",
        help='Archive file to skip already-downloaded videos (default: "downloaded_archive.txt")',
    )
    parser.add_argument(
        "--cookies-file",
        help="Optional path to an exported YouTube cookies.txt file for restricted videos",
    )
    parser.add_argument(
        "--ffmpeg-location",
        help="Optional path to ffmpeg/ffprobe if not in PATH",
    )

    args = parser.parse_args()

    channel_url = get_channel_url(args.channel_url)
    output_dir = Path(args.output_dir).expanduser().resolve()
    archive_file = Path(args.archive_file).expanduser().resolve()

    cookies_file = None
    if args.cookies_file:
        cookies_file = Path(args.cookies_file).expanduser().resolve()
        if not cookies_file.is_file():
            raise SystemExit(f"Cookies file not found: {cookies_file}")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_file.parent.mkdir(parents=True, exist_ok=True)

    check_yt_dlp_installed()

    cmd = build_command(
        channel_url=channel_url,
        output_dir=output_dir,
        archive_file=archive_file,
        ffmpeg_location=args.ffmpeg_location,
        cookies_file=cookies_file,
    )

    print("\nRunning:\n")
    print(" ".join(shlex.quote(part) for part in cmd))
    print()

    try:
        completed = subprocess.run(cmd, check=False)
        return completed.returncode
    except KeyboardInterrupt:
        print("\nStopped by user.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
