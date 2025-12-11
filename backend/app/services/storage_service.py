"""
Storage Service.
Handles file storage operations with Supabase Storage.
"""

from typing import Optional
import os
import aiofiles
import logging

from app.config import settings

logger = logging.getLogger(__name__)

# Local upload directory for development
UPLOAD_DIR = "uploads"


class StorageService:
    """
    Service for file storage operations.
    Uses local filesystem in development, Supabase Storage in production.
    """

    def __init__(self):
        """Initialize storage service."""
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # In production, initialize Supabase client here
        self.supabase = None

    async def upload(
        self,
        file_path: str,
        content: bytes,
        content_type: str
    ) -> str:
        """
        Upload a file to storage.

        Args:
            file_path: Path to store the file (e.g., "user_id/file_id.pdf")
            content: File bytes
            content_type: MIME type

        Returns:
            Storage path
        """
        if self.supabase:
            # Production: Upload to Supabase Storage
            return await self._upload_supabase(file_path, content, content_type)
        else:
            # Development: Save to local filesystem
            return await self._upload_local(file_path, content)

    async def _upload_local(self, file_path: str, content: bytes) -> str:
        """Save file to local filesystem."""
        full_path = os.path.join(UPLOAD_DIR, file_path)

        # Create directory if needed
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        async with aiofiles.open(full_path, "wb") as f:
            await f.write(content)

        logger.info(f"File saved locally: {full_path}")
        return file_path

    async def _upload_supabase(
        self,
        file_path: str,
        content: bytes,
        content_type: str
    ) -> str:
        """Upload file to Supabase Storage."""
        # This would use the Supabase client in production
        # Example:
        # response = self.supabase.storage.from_("documents").upload(
        #     file_path, content, {"content-type": content_type}
        # )
        raise NotImplementedError("Supabase storage not configured")

    async def download(self, file_path: str) -> bytes:
        """
        Download a file from storage.
        """
        if self.supabase:
            return await self._download_supabase(file_path)
        else:
            return await self._download_local(file_path)

    async def _download_local(self, file_path: str) -> bytes:
        """Read file from local filesystem."""
        full_path = os.path.join(UPLOAD_DIR, file_path)

        async with aiofiles.open(full_path, "rb") as f:
            return await f.read()

    async def _download_supabase(self, file_path: str) -> bytes:
        """Download file from Supabase Storage."""
        raise NotImplementedError("Supabase storage not configured")

    async def delete(self, file_path: str) -> bool:
        """
        Delete a file from storage.
        """
        if self.supabase:
            return await self._delete_supabase(file_path)
        else:
            return await self._delete_local(file_path)

    async def _delete_local(self, file_path: str) -> bool:
        """Delete file from local filesystem."""
        full_path = os.path.join(UPLOAD_DIR, file_path)

        try:
            os.remove(full_path)
            logger.info(f"File deleted: {full_path}")
            return True
        except FileNotFoundError:
            logger.warning(f"File not found for deletion: {full_path}")
            return False

    async def _delete_supabase(self, file_path: str) -> bool:
        """Delete file from Supabase Storage."""
        raise NotImplementedError("Supabase storage not configured")

    async def get_signed_url(
        self,
        file_path: str,
        expires_in: int = 3600
    ) -> str:
        """
        Get a signed URL for file download.

        Args:
            file_path: Storage path
            expires_in: URL validity in seconds

        Returns:
            Signed download URL
        """
        if self.supabase:
            # Production: Generate Supabase signed URL
            # response = self.supabase.storage.from_("documents").create_signed_url(
            #     file_path, expires_in
            # )
            # return response["signedURL"]
            raise NotImplementedError("Supabase storage not configured")
        else:
            # Development: Return local path (not a real URL)
            return f"/api/documents/download/{file_path}"

    async def get_file_size(self, file_path: str) -> int:
        """Get the size of a stored file."""
        full_path = os.path.join(UPLOAD_DIR, file_path)
        return os.path.getsize(full_path)
