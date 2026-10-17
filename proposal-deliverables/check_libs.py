try:
    import docx  # noqa: F401

    print("python-docx available")
except ImportError:
    print("python-docx NOT available")

try:
    import pptx  # noqa: F401

    print("python-pptx available")
except ImportError:
    print("python-pptx NOT available")
