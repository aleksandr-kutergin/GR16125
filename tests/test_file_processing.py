from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from fastapi import UploadFile

from app.file_processing import (_search_in_file, process_csv_file,
                                 process_txt_file)


@pytest.mark.asyncio
async def test_search_in_file_found():
    mock_upload_file = AsyncMock(spec=UploadFile)
    mock_file = AsyncMock()
    mock_upload_file.file = mock_file
    mock_file.readline = Mock(
        side_effect=[
            b"This is a test file with quantori.\n" b"",
        ]
    )
    result = await _search_in_file(mock_upload_file)

    assert result is True


@pytest.mark.asyncio
async def test_search_in_file_not_found():
    mock_upload_file = AsyncMock(spec=UploadFile)

    mock_file = AsyncMock()
    mock_upload_file.file = mock_file

    mock_file.readline = Mock(
        side_effect=[
            b"This is a test file without the keyword.\n",
            b"",
        ]
    )

    result = await _search_in_file(mock_upload_file)

    assert result is False


@pytest.mark.asyncio
async def test_process_txt_file(mock_db, mock_user):
    user_id = 1
    file_mock = MagicMock()
    file_mock.filename = "test_file.txt"

    with patch("app.file_processing._search_in_file", return_value=True):
        with patch("app.file_processing.save_file", return_value=1):
            result = await process_txt_file(file_mock, mock_db, user_id)
            assert result["filename"] == "test_file.txt"
            assert result["file_type"] == "txt"
            assert result["result_found"] is True
            assert result["user_id"] == user_id
            assert result["id"] == 1


@pytest.mark.skip("hangs")
@pytest.mark.asyncio
async def test_process_txt_file_not_found(mock_db, mock_user):
    user_id = 1
    file_mock = MagicMock()
    file_mock.filename = "test_file.txt"

    contents = "Header\nanother company\nyet another company"
    file_mock.read = AsyncMock(return_value=contents.encode())
    with patch("app.file_processing.save_file", return_value=1):
        result = await process_txt_file(file_mock, mock_db, user_id)

    assert result["filename"] == "test_file.txt"
    assert result["file_type"] == "txt"
    assert result["result_found"] is False
    assert result["user_id"] == user_id
    assert result["id"] == 1


@pytest.mark.asyncio
async def test_process_csv_file(mock_db, mock_user):
    user_id = 1
    file_mock = MagicMock()
    file_mock.filename = "test_file.csv"

    contents = "Company Name\nquantori\nother name"
    file_mock.read = AsyncMock(return_value=contents.encode())
    with patch("app.file_processing.save_file", return_value=1):
        result = await process_csv_file(file_mock, mock_db, user_id)

    assert result["filename"] == "test_file.csv"
    assert result["file_type"] == "csv"
    assert result["result_found"] is True
    assert result["user_id"] == 1


@pytest.mark.asyncio
async def test_process_csv_file_not_found(mock_db, mock_user):
    user_id = 1
    file_mock = MagicMock()
    file_mock.filename = "test_file.csv"

    contents = "Company Name\nanother company\nanother company"
    file_mock.read = AsyncMock(return_value=contents.encode())
    with patch("app.file_processing.save_file", return_value=1):
        result = await process_csv_file(file_mock, mock_db, user_id)

    assert result["filename"] == "test_file.csv"
    assert result["file_type"] == "csv"
    assert result["result_found"] is False
    assert result["user_id"] == user_id
    assert result["id"] == 1
