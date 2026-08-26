from langchain_community.document_loaders import YoutubeLoader


def transcript_loader(url: str):
    """Download a YouTube transcript in English or Hindi."""
    loader = YoutubeLoader.from_youtube_url(url, language=["en", "hi"])
    return loader.load()
