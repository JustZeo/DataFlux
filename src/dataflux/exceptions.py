class DataFluxError(Exception):
    """Base exception for all DataFlux errors."""


# ============================================================================
# Provider Errors
# ============================================================================

class InvalidProviderError(DataFluxError):
    """Raised when an invalid provider is supplied."""


class ProviderAlreadyRegisteredError(DataFluxError):
    """Raised when a provider with the same name is already registered."""

    def __init__(self, provider_name: str):
        super().__init__(
            f"Provider '{provider_name}' is already registered."
        )


class ProviderNotFoundError(DataFluxError):
    """Raised when a requested provider does not exist."""

    def __init__(self, provider_name: str):
        super().__init__(
            f"Provider '{provider_name}' was not found."
        )


# ============================================================================
# Dataset Errors
# ============================================================================

class DatasetNotFoundError(DataFluxError):
    """Raised when no dataset matches the query."""

    def __init__(self, dataset: str | int):
        super().__init__(
            f"Dataset '{dataset}' was not found."
        )


class InvalidDatasetError(DataFluxError):
    """Raised when a dataset identifier is invalid."""

    def __init__(self, dataset: str | int):
        super().__init__(
            f"'{dataset}' is not a valid dataset identifier."
        )


class DatasetLoadError(DataFluxError):
    """Raised when a dataset cannot be loaded."""

    def __init__(self, dataset: str | int):
        super().__init__(
            f"Failed to load dataset '{dataset}'."
        )


# ============================================================================
# Search Errors
# ============================================================================

class SearchError(DataFluxError):
    """Raised when a search operation fails."""


class EmptySearchQueryError(SearchError):
    """Raised when an empty search query is provided."""

    def __init__(self):
        super().__init__(
            "Search query cannot be empty."
        )


# ============================================================================
# Pull Errors
# ============================================================================

class PullError(DataFluxError):
    """Raised when pulling a dataset fails."""


# ============================================================================
# Download Errors
# ============================================================================

class DownloadError(DataFluxError):
    """Raised when a download operation fails."""

    def __init__(self, url: str):
        super().__init__(
            f"Failed to download resource from '{url}'."
        )


# ============================================================================
# Cache Errors
# ============================================================================

class CacheError(DataFluxError):
    """Raised when a cache operation fails."""


# ============================================================================
# Filesystem Errors
# ============================================================================

class FileSystemError(DataFluxError):
    """Raised when a filesystem operation fails."""


# ============================================================================
# Export Errors
# ============================================================================

class ExportError(DataFluxError):
    """Raised when exporting a dataset fails."""


class UnsupportedExportFormatError(ExportError):
    """Raised when an unsupported export format is requested."""

    def __init__(self, extension: str):
        super().__init__(
            f"Export format '{extension}' is not supported."
        )


class ExportFileExistsError(ExportError):
    """Raised when the export file already exists."""

    def __init__(self, path: str):
        super().__init__(
            f"'{path}' already exists. "
            "Use overwrite=True to replace it."
        )


class InvalidExportDataError(ExportError):
    """Raised when the object being exported is invalid."""

    def __init__(
        self,
        message: str = "export() expects a Polars DataFrame.",
    ):
        super().__init__(message)