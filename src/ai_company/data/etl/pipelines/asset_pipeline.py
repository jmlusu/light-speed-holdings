"""Asset pipeline and performance optimization for media and file assets.

Implements caching, resizing, optimization, and performance tracking for
images, documents, and other media assets used across the AI Company Builder
platform. Integrates with ComfyUI for image generation and faster-whisper
for transcription, providing a unified asset management layer.

Key features:
- Asset caching with TTL and size-based eviction
- Image resizing and format optimization
- Transcription result caching
- Performance metrics and cost tracking
- Integration with existing ComfyUI and transcription pipelines
"""

from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Default cache directories
DEFAULT_CACHE_DIR = Path(".asset_cache")
DEFAULT_TTL_SECONDS = 86400  # 24 hours
MAX_CACHE_SIZE_GB = 10.0

# Image optimization settings
MAX_IMAGE_WIDTH = 2048
MAX_IMAGE_HEIGHT = 2048
SUPPORTED_IMAGE_FORMATS = {"png", "jpg", "jpeg", "webp", "gif"}
DEFAULT_IMAGE_QUALITY = 85

# Asset types
ASSET_TYPE_IMAGE = "image"
ASSET_TYPE_TRANSCRIPTION = "transcription"
ASSET_TYPE_DOCUMENT = "document"
ASSET_TYPE_VIDEO = "video"


@dataclass
class AssetMetadata:
    """Metadata for an cached asset."""

    asset_type: str
    original_path: Path
    asset_hash: str
    file_size: int
    mime_type: str
    created_at: float = field(default_factory=time.time)
    accessed_at: float = field(default_factory=time.time)
    ttl_seconds: float = DEFAULT_TTL_SECONDS
    resize_width: int | None = None
    resize_height: int | None = None
    format: str | None = None


@dataclass
class AssetCacheEntry:
    """An entry in the asset cache."""

    metadata: AssetMetadata
    file_path: Path
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0


@dataclass
class PerformanceMetrics:
    """Performance metrics for asset operations."""

    total_assets_cached: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    total_resize_operations: int = 0
    total_transcode_operations: int = 0
    total_cache_evictions: int = 0
    average_access_time_ms: float = 0.0


class AssetPipeline:
    """Manages asset caching, optimization, and performance tracking.

    Provides a unified interface for:
    - Caching assets (images, transcriptions, documents)
    - Resizing and format optimization
    - Performance metrics collection
    - Integration with ComfyUI and transcription pipelines
    """

    def __init__(
        self,
        cache_dir: Path | None = None,
        ttl_seconds: int = DEFAULT_TTL_SECONDS,
        max_cache_size_gb: float = MAX_CACHE_SIZE_GB,
    ) -> None:
        """Initialize the asset pipeline.

        Args:
            cache_dir: Directory for cached assets (defaults to .asset_cache)
            ttl_seconds: Time-to-live for cached assets in seconds
            max_cache_size_gb: Maximum cache size in GB
        """
        self._cache_dir = (cache_dir or DEFAULT_CACHE_DIR).resolve()
        self._ttl_seconds = ttl_seconds
        self._max_cache_size_bytes = int(max_cache_size_gb * 1024 * 1024)
        self._metrics = PerformanceMetrics()
        self._cache: dict[str, AssetCacheEntry] = {}
        self._cache_dir.mkdir(parents=True, exist_ok=True)

        # Scan existing cache on init
        self._scan_cache()

    def _scan_cache(self) -> None:
        """Scan the cache directory and rebuild the in-memory cache index."""
        if not self._cache_dir.exists():
            return

        for file_path in self._cache_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower().lstrip(".") in {
                *SUPPORTED_IMAGE_FORMATS,
                "mp3",
                "wav",
                "m4a",
                "txt",
                "pdf",
            }:
                try:
                    stat = file_path.stat()
                    asset_hash = self._compute_hash(file_path)
                    mime_type = self._guess_mime_type(file_path.suffix.lstrip("."))

                    entry = AssetCacheEntry(
                        metadata=AssetMetadata(
                            asset_type=self._determine_type(file_path.suffix.lstrip(".")),
                            original_path=file_path,
                            asset_hash=asset_hash,
                            file_size=stat.st_size,
                            mime_type=mime_type,
                        ),
                        file_path=file_path,
                    )
                    self._cache[asset_hash] = entry
                except OSError:
                    pass  # Skip files we can't stat

    @staticmethod
    def _compute_hash(file_path: Path) -> str:
        """Compute SHA256 hash of a file for deduplication."""
        h = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            return h.hexdigest()
        except OSError:
            return ""

    @staticmethod
    def _guess_mime_type(ext: str) -> str:
        """Guess MIME type from file extension."""
        mime_map = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "webp": "image/webp",
            "gif": "image/gif",
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "m4a": "audio/m4a",
            "txt": "text/plain",
            "pdf": "application/pdf",
        }
        return mime_map.get(ext.lower(), "application/octet-stream")

    @staticmethod
    def _determine_type(ext: str) -> str:
        """Determine asset type from file extension."""
        image_exts = {"png", "jpg", "jpeg", "webp", "gif"}
        if ext.lower() in image_exts:
            return ASSET_TYPE_IMAGE
        if ext.lower() in {"mp3", "wav", "m4a"}:
            return ASSET_TYPE_TRANSCRIPTION
        if ext.lower() in {"pdf", "txt"}:
            return ASSET_TYPE_DOCUMENT
        return ASSET_TYPE_VIDEO

    def get_cached_asset(self, identifier: str) -> AssetCacheEntry | None:
        """Retrieve a cached asset by identifier (hash or path).

        Args:
            identifier: SHA256 hash or file path string

        Returns:
            AssetCacheEntry if found and not expired, None otherwise
        """
        # Try hash lookup first
        if identifier in self._cache:
            entry: AssetCacheEntry = self._cache[identifier]
            if self._is_expired(entry):
                self._remove_entry(identifier)
                self._metrics.cache_misses += 1
                return None
            entry.metadata.accessed_at = time.time()
            entry.access_count += 1
            self._metrics.cache_hits += 1
            self._enforce_size_limit()
            return entry

        # Try path lookup (re-scan)
        path = Path(identifier)
        if path.exists():
            asset_hash = self._compute_hash(path)
        if asset_hash in self._cache:
            entry = self._cache[asset_hash]  # reuse entry variable in new scope
            if self._is_expired(entry):
                self._remove_entry(asset_hash)
                self._metrics.cache_misses += 1
                return None
            entry.metadata.accessed_at = time.time()
            entry.access_count += 1
            self._metrics.cache_hits += 1
            self._enforce_size_limit()
            return entry

        self._metrics.cache_misses += 1
        return None

    def _is_expired(self, entry: AssetCacheEntry) -> bool:
        """Check if a cache entry has expired based on TTL."""
        return (time.time() - entry.metadata.created_at) > self._ttl_seconds

    def _remove_entry(self, identifier: str) -> None:
        """Remove a cache entry from memory and disk."""
        if identifier in self._cache:
            entry = self._cache.pop(identifier)
            try:
                if entry.file_path.exists():
                    entry.file_path.unlink()
            except OSError:
                pass

    def _enforce_size_limit(self) -> None:
        """Enforce maximum cache size by evicting oldest/least-used entries."""
        total_size = sum(entry.metadata.file_size for entry in self._cache.values())

        while total_size > self._max_cache_size_bytes and self._cache:
            # Find oldest or least-accessed entry for eviction
            oldest_key = min(
                self._cache.keys(),
                key=lambda k: self._cache[k].last_accessed,
            )
            evicted = self._cache.pop(oldest_key)
            try:
                if evicted.file_path.exists():
                    evicted.file_path.unlink()
            except OSError:
                pass
            self._metrics.total_cache_evictions += 1
            total_size -= evicted.metadata.file_size

    def cache_asset(
        self,
        asset_data: bytes,
        metadata: AssetMetadata,
    ) -> AssetCacheEntry:
        """Cache an asset with the given metadata.

        Args:
            asset_data: Raw bytes of the asset
            metadata: Asset metadata including type, path, hash, etc.

        Returns:
            The created AssetCacheEntry
        """
        asset_hash = self._compute_hash_from_bytes(asset_data)

        # Determine file extension from mime_type if available, else default
        mime_to_ext = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/webp": ".webp",
            "text/plain": ".txt",
            "application/pdf": ".pdf",
        }
        ext = mime_to_ext.get(metadata.mime_type, ".bin")

        cache_path = self._cache_dir / f"{asset_hash}{ext}"

        # Write file
        try:
            cache_path.write_bytes(asset_data)
        except OSError as exc:
            logger.error("Failed to write asset cache: %s", exc)
            raise

        # Update metadata with actual file path
        metadata = AssetMetadata(
            asset_type=metadata.asset_type,
            original_path=metadata.original_path,
            asset_hash=asset_hash,
            file_size=metadata.file_size,
            mime_type=metadata.mime_type,
            created_at=time.time(),
            accessed_at=time.time(),
            ttl_seconds=self._ttl_seconds,
        )

        entry = AssetCacheEntry(
            metadata=metadata,
            file_path=cache_path,
        )
        self._cache[asset_hash] = entry

        # Enforce size limit after adding
        self._enforce_size_limit()

        self._metrics.total_assets_cached += 1
        return entry

    @staticmethod
    def _compute_hash_from_bytes(data: bytes) -> str:
        """Compute SHA256 hash from bytes."""
        return hashlib.sha256(data).hexdigest()

    def resize_image(
        self,
        input_path: Path,
        output_path: Path | None = None,
        max_width: int = MAX_IMAGE_WIDTH,
        max_height: int | None = MAX_IMAGE_HEIGHT,
        quality: int = DEFAULT_IMAGE_QUALITY,
        format: str | None = None,
    ) -> Path:
        """Resize and optimize an image asset.

        Uses PIL/Pillow for image processing. If the image is already within
        the max dimensions, it is returned unchanged (except for format/quality
        optimization).

        Args:
            input_path: Path to the input image
            output_path: Path for the output image (defaults to input with suffix)
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            quality: JPEG/WebP quality (1-100)
            format: Output format (png, jpg, webp)

        Returns:
            Path to the optimized image
        """
        try:
            from PIL import Image
        except ImportError:
            logger.warning("Pillow not installed; skipping image resize")
            return input_path

        output_path = output_path or input_path
        try:
            with Image.open(input_path) as img:
                # Calculate new dimensions if needed
                width, height = img.size

                if width > max_width or (max_height is not None and height > max_height):
                    # Calculate ratio to fit within max dimensions
                    if max_width > 0 and max_height is not None:
                        ratio = min(max_width / width, max_height / height)
                    elif max_width > 0:
                        ratio = max_width / width
                    elif max_height is not None and height > 0:
                        ratio = max_height / height
                    else:
                        ratio = 1.0
                    new_width = int(width * ratio)
                    new_height = int(height * ratio)
                    processed_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                else:
                    new_width, new_height = width, height

                # Determine output format
                out_format = format or img.format or "PNG"
                if out_format not in ("PNG", "JPEG", "WEBP"):
                    out_format = "PNG"

                # Save optimized
                save_kwargs: dict[str, Any] = {}
                if out_format in ("JPEG", "JPG"):
                    save_kwargs["quality"] = quality
                    save_kwargs["optimize"] = True
                elif out_format == "WEBP":
                    save_kwargs["quality"] = quality
                    save_kwargs["method"] = 6  # Best compression

                # Convert RGBA to RGB for JPEG if needed
                processed_img = img
                if out_format in ("JPEG", "JPG") and processed_img.mode == "RGBA":
                    background = Image.new("RGB", processed_img.size, (255, 255, 255))
                    background.paste(processed_img, mask=processed_img.split()[3])
                    processed_img = background

                if out_format == "PNG" and processed_img.mode != "RGBA":
                    processed_img = processed_img.convert("RGBA")

                processed_img.save(output_path, format=out_format, **save_kwargs)

                # Update metrics
                self._metrics.total_resize_operations += 1

                return output_path

        except Exception as exc:  # noqa: BLE001 - log and return input
            logger.error("Image resize failed for %s: %s", input_path, exc)
            return input_path

    def get_metrics(self) -> PerformanceMetrics:
        """Return current performance metrics."""
        return self._metrics

    def reset_metrics(self) -> None:
        """Reset all performance metrics."""
        self._metrics = PerformanceMetrics()


# Convenience function for quick asset operations
def create_pipeline(
    cache_dir: str | Path | None = None,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
) -> AssetPipeline:
    """Create an AssetPipeline instance with the given configuration.

    Args:
        cache_dir: Directory for cached assets
        ttl_seconds: Time-to-live for cached assets

    Returns:
        Configured AssetPipeline instance
    """
    final_cache_dir = Path(cache_dir) if cache_dir is not None else None
    return AssetPipeline(cache_dir=final_cache_dir, ttl_seconds=ttl_seconds)
