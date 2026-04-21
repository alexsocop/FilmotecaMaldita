#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from pathlib import Path

DEFAULT_CHANNEL = "https://www.youtube.com/@Lafilmotecamaldita/videos"
YOUTUBE_WATCH_URL = "https://www.youtube.com/watch?v={video_id}"

VIDEO_ID_RE = re.compile(r"\[([A-Za-z0-9_-]{11})\]\.(?:mkv|MKV)$")


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
            f'Install it with:\n  {sys.executable} -m pip install -U --pre "yt-dlp[default]"\n'
        ) from exc


def common_yt_dlp_args(
    ffmpeg_location: str | None,
    cookies_file: Path | None,
) -> list[str]:
    args = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--ignore-errors",
        "--continue",
        "--no-overwrites",
        "--retries", "10",
        "--fragment-retries", "10",
        "--sleep-interval", "5",
        "--max-sleep-interval", "10",
        "--remote-components", "ejs:github",
        "--js-runtimes", "deno",
        "-f", "bv*+ba/b",
        "--merge-output-format", "mkv",
        "--write-info-json",
        "--write-description",
        "--no-write-playlist-metafiles",
        "--embed-metadata",
        "--embed-chapters",
        "--write-thumbnail",
        "--convert-thumbnails", "jpg",
    ]

    if cookies_file is not None:
        args.extend(["--cookies", str(cookies_file)])

    if ffmpeg_location:
        args.extend(["--ffmpeg-location", ffmpeg_location])

    return args


def build_channel_download_command(
    channel_url: str,
    output_dir: Path,
    archive_file: Path,
    ffmpeg_location: str | None,
    cookies_file: Path | None,
) -> list[str]:
    cmd = common_yt_dlp_args(ffmpeg_location, cookies_file)
    cmd.extend([
        "--download-archive", str(archive_file),
        "-o",
        str(output_dir / "%(channel|uploader)s/%(upload_date>%Y-%m-%d)s - %(title)s [%(id)s].%(ext)s"),
        channel_url,
    ])
    return cmd


def build_refresh_command_for_file(
    file_path: Path,
    video_id: str,
    ffmpeg_location: str | None,
    cookies_file: Path | None,
) -> list[str]:
    exact_output_template = str(file_path.with_suffix(".%(ext)s"))

    cmd = common_yt_dlp_args(ffmpeg_location, cookies_file)
    cmd.extend([
        "-o", exact_output_template,
        YOUTUBE_WATCH_URL.format(video_id=video_id),
    ])
    return cmd


def find_existing_downloads(output_dir: Path) -> list[tuple[Path, str]]:
    results: list[tuple[Path, str]] = []

    if not output_dir.exists():
        return results

    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() != ".mkv":
            continue

        match = VIDEO_ID_RE.search(path.name)
        if match:
            results.append((path, match.group(1)))

    results.sort(key=lambda item: str(item[0]).lower())
    return results


def refresh_metadata_for_existing_files(
    output_dir: Path,
    ffmpeg_location: str | None,
    cookies_file: Path | None,
    start_index: int,
    limit: int | None,
) -> int:
    existing_files = find_existing_downloads(output_dir)

    if not existing_files:
        print("\nNo existing .mkv files with [video_id] found. Skipping metadata refresh.\n")
        return 0

    total = len(existing_files)

    if start_index < 1:
        raise SystemExit("--refresh-start-index must be 1 or higher")

    start_pos = start_index - 1
    if start_pos >= total:
        raise SystemExit(
            f"--refresh-start-index {start_index} is beyond the number of existing files ({total})"
        )

    selected = existing_files[start_pos:]
    if limit is not None:
        if limit < 1:
            raise SystemExit("--refresh-limit must be 1 or higher")
        selected = selected[:limit]

    print(
        f"\nRefreshing metadata for {len(selected)} existing file(s) "
        f"(starting at item {start_index} of {total})...\n"
    )

    failures = 0

    for idx, (file_path, video_id) in enumerate(selected, start=start_index):
        print(f"[{idx}/{total}] Refreshing metadata for: {file_path.name}")
        cmd = build_refresh_command_for_file(
            file_path=file_path,
            video_id=video_id,
            ffmpeg_location=ffmpeg_location,
            cookies_file=cookies_file,
        )

        completed = subprocess.run(cmd, check=False)
        if completed.returncode != 0:
            failures += 1
            print(f"  Warning: metadata refresh failed for {file_path.name}\n")
        else:
            print()

    print(f"Metadata refresh finished. Failures: {failures}\n")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Download new videos from a YouTube channel with metadata, and optionally "
            "refresh metadata for already-downloaded videos in small batches."
        )
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
    parser.add_argument(
        "--refresh-existing-metadata",
        action="store_true",
        help="Refresh metadata for already-downloaded videos before the normal channel pass",
    )
    parser.add_argument(
        "--refresh-only",
        action="store_true",
        help="Refresh metadata only; do not run the normal new-download pass",
    )
    parser.add_argument(
        "--refresh-start-index",
        type=int,
        default=1,
        help="1-based starting index for metadata refresh batches (default: 1)",
    )
    parser.add_argument(
        "--refresh-limit",
        type=int,
        help="Maximum number of existing files to refresh in this run",
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

    refresh_failures = 0

    if args.refresh_existing_metadata or args.refresh_only:
        if cookies_file is None:
            raise SystemExit(
                "Refreshing existing metadata is disabled unless you provide --cookies-file.\n"
                "This avoids triggering YouTube's bot checks when revisiting many old videos.\n"
                "Use a fresh exported cookies.txt from a private/incognito session."
            )

        refresh_failures = refresh_metadata_for_existing_files(
            output_dir=output_dir,
            ffmpeg_location=args.ffmpeg_location,
            cookies_file=cookies_file,
            start_index=args.refresh_start_index,
            limit=args.refresh_limit,
        )

    if args.refresh_only:
        return 1 if refresh_failures else 0

    download_cmd = build_channel_download_command(
        channel_url=channel_url,
        output_dir=output_dir,
        archive_file=archive_file,
        ffmpeg_location=args.ffmpeg_location,
        cookies_file=cookies_file,
    )

    print("Running new-download pass:\n")
    print(" ".join(shlex.quote(part) for part in download_cmd))
    print()

    try:
        completed = subprocess.run(download_cmd, check=False)
        if completed.returncode != 0:
            return completed.returncode
        return 1 if refresh_failures else 0
    except KeyboardInterrupt:
        print("\nStopped by user.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
