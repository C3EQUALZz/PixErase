from pix_erase.application.queries.images.reverse_search_image import (
    ReverseImageSearchQuery,
    ReverseImageSearchQueryHandler,
)


def test_reverse_image_search_placeholder() -> None:
    # Handler is not implemented yet; keep placeholder to signal coverage intent.
    assert ReverseImageSearchQuery is not None
    assert ReverseImageSearchQueryHandler is not None
